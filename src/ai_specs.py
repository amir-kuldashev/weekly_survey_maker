"""Short complaint specifications for the weekly report, written by Gemini.

For every location bullet in "Weekly complaints by location" whose category is
not covered by the confirmed-case text (Vehicle Conditions, Vehicle
Cleanlines, Shuttle Service, Reserved Vehicle Unavailable) the report lists
each complaint as "R/A NUMBER - specification", e.g.
"LGA-99773 - bad smell; LGA-99558 - dirty vehicle;".

The specification is a summary of at most 3 words of what the customer wrote about that
category, produced by one Gemini request per report (free tier is enough for a
weekly run). Without an API key, or if the request fails, the bullets fall
back to the R/A numbers alone so the report still generates.
"""
import json
import os
import time
import urllib.error
import urllib.request

from .context import context
from .weekly_complaints_by_location_category import CONFIRMED_BULLETS
from .const import BULLET_CATEGORIES

# Categories whose bullet text is written by the AI.
AI_CATEGORIES = [c for c in BULLET_CATEGORIES if c not in CONFIRMED_BULLETS]

GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
# Tried in order when a model is overloaded (503), rate limited (429) or retired (404).
FALLBACK_MODELS = [DEFAULT_MODEL, "gemini-3.8-flash", "gemini-3.5-flash", "gemini-flash-lite-latest"]
RETRY_WAITS = (2, 5)  # seconds between attempts on the same model
REQUEST_TIMEOUT = 45  # seconds per attempt
TOTAL_DEADLINE = 150  # seconds for the whole AI step; after this the report continues without it
NO_DETAILS = "no details given"
MAX_SPEC_WORDS = 3

SYSTEM_PROMPT = """You help write an internal weekly customer-service report for a car rental company.
You receive customer complaints. Each item has an id, a category, and the customer's text.
For each item write a very short specification of AT MOST 3 words (lower case, no trailing period) that says
ONLY what the customer wrote about the given category. Ignore anything about other topics.
Examples: "bad smell", "dirty vehicle", "low tires", "old scratched car", "food inside", "car shaking",
"long shuttle wait", "suv unavailable".
If the text says nothing about the category, or is empty, answer exactly "no details given".
Return one result per item, keeping the id and category unchanged."""

RESPONSE_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "category": {"type": "string"},
            "spec": {"type": "string"},
        },
        "required": ["id", "category", "spec"],
    },
}


def collect_items(weekly_data):
    """Complaints the AI should describe: non-duplicate survey + call center rows
    flagged in an AI category. One item per (R/A, category)."""
    non_duplicate = weekly_data[weekly_data["Duplicate?"] == "No"]
    rows = non_duplicate[non_duplicate["Source"].isin(["Drivo Survey", "Call Center"])]
    items = []
    for _, row in rows.iterrows():
        ra = str(row.get("R/A OR CONFIRMATION", "") or "").strip()
        text = row.get("Complaint Overview", "")
        text = "" if text is None or (isinstance(text, float)) else str(text).strip()
        for category in AI_CATEGORIES:
            if row.get(category) == "Yes":
                items.append({"id": ra or "Unknown", "location": row.get("Location"),
                              "category": category, "text": text})
    return items


def ask_gemini(items, api_key, model=DEFAULT_MODEL, timeout=REQUEST_TIMEOUT):
    """One request for all items. Returns {(id, category): spec}."""
    payload = [{"id": it["id"], "category": it["category"], "text": it["text"] or "(empty)"}
               for it in items]
    body = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": json.dumps(payload, ensure_ascii=False)}]}],
        "generationConfig": {
            "temperature": 0,
            "responseMimeType": "application/json",
            "responseSchema": RESPONSE_SCHEMA,
        },
    }
    url = GEMINI_ENDPOINT.format(model=model) + "?key=" + api_key
    request = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))
    candidate = (data.get("candidates") or [{}])[0]
    parts = (candidate.get("content") or {}).get("parts") or []
    if not parts or "text" not in parts[0]:
        reason = candidate.get("finishReason") or (data.get("promptFeedback") or {}).get("blockReason") or "no text returned"
        raise ValueError(f"empty answer ({reason})")
    results = json.loads(parts[0]["text"])
    specs = {}
    for r in results:
        spec = str(r.get("spec", "")).strip().rstrip(".").strip()
        if spec != NO_DETAILS:
            spec = " ".join(spec.split()[:MAX_SPEC_WORDS])  # hard cap, even if the model rambles
        if spec:
            specs[(str(r.get("id", "")).strip(), r.get("category", ""))] = spec
    return specs


def ask_with_retries(items, api_key):
    """Try each model in FALLBACK_MODELS; retry overload / rate-limit answers."""
    last_error = "no models tried"
    seen = []
    started = time.monotonic()
    for model in FALLBACK_MODELS:
        if model in seen:
            continue
        seen.append(model)
        for attempt, wait in enumerate((0,) + RETRY_WAITS):
            remaining = TOTAL_DEADLINE - (time.monotonic() - started)
            if remaining <= 5:
                return {}, f"Gemini request failed - gave up after {TOTAL_DEADLINE}s ({last_error})"
            if wait:
                time.sleep(wait)
            try:
                specs = ask_gemini(items, api_key, model=model, timeout=min(REQUEST_TIMEOUT, remaining))
                described = sum(1 for it in items if (it["id"], it["category"]) in specs)
                return specs, f"Gemini ({model}) described {described} of {len(items)} complaints"
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "replace")
                try:
                    detail = json.loads(detail)["error"]["message"]
                except (ValueError, KeyError, TypeError):
                    pass
                last_error = f"{model}: HTTP {e.code} {detail[:200]}"
                if e.code in (429, 503):
                    continue          # same model, retry after the wait
                break                 # 404 retired model, 400 bad key, ...: next model
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                last_error = f"{model}: unreachable ({e})"
                continue
            except (KeyError, IndexError, ValueError, TypeError) as e:
                last_error = f"{model}: answer could not be read ({e})"
                break
    return {}, f"Gemini request failed - {last_error}"


def format_bullet(items_for_bullet, specs):
    """'RA - spec; RA - spec;' in the order the complaints appear."""
    parts = []
    for it in items_for_bullet:
        spec = specs.get((it["id"], it["category"])) if specs else None
        if spec:
            parts.append(f"{it['id']} - {spec}")
        elif not it["text"]:
            parts.append(f"{it['id']} - {NO_DETAILS}")
        else:
            parts.append(it["id"])
    return "; ".join(parts) + (";" if parts else "")


def apply_ai_specifications(weekly_data, api_key=None):
    """Fill the AI-category bullet descriptions in context['narrative_lists']."""
    items = collect_items(weekly_data)
    specs = {}
    status = "no complaints in AI categories"
    if items:
        api_key = (api_key or os.environ.get("GEMINI_API_KEY") or "").strip()
        if not api_key:
            status = "no Gemini API key - bullets list R/A numbers only"
        else:
            specs, status = ask_with_retries(items, api_key)
    context["ai_specs_status"] = status
    print(status)

    for loc in context.get("narrative_lists", []):
        for bullet in loc["bullets"]:
            if bullet["title"] not in AI_CATEGORIES:
                continue
            mine = [it for it in items if it["location"] == loc["name"] and it["category"] == bullet["title"]]
            if mine:
                bullet["description"] = format_bullet(mine, specs)
    return status
