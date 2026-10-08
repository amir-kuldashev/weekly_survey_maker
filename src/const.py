locations = ["EWR", "EWRCON", "JFK", "LGA", "BRK", "BRKJS"]


def normalize_location(value):
    """Clean a raw location code from the R/A export or CS database.

    Codes are stripped and upper-cased so e.g. " ewrcon" matches "EWRCON".
    Every code is reported as its own location (EWRCON is NOT folded into EWR).
    """
    if not isinstance(value, str):
        return value
    return value.strip().upper()


def safe_pct(numerator, denominator, digits=2):
    """Percentage that returns 0 instead of raising when the denominator is 0.

    Small locations (e.g. EWRCON) can have no closed R/As in a given week.
    """
    if not denominator:
        return 0
    return round(float(numerator) / float(denominator) * 100, digits)

ALL_COMPLAINTS = [
    "Upsell complaints",
    "Unexpected Fees",
    "Vehicle Conditions",
    "Vehicle Cleanlines",
    "Long wait",
    "Long shuttle",
    "Shuttle Service",
    "Location Complaint",
    "Geozone",
    "Damage Claims",
    "Rude service",
    "Unhelpful Service",
    "Reserved Vehicle Unavailable",
    "Call Center Complaints",
    "Deposit Hold",
    "Insurance Verification",
    "Tolls and Violations",
    "Credit Check",
    "Other Complaints",
    "No Information"
]

CATEGORY_STYLES = {
    "Upsell complaints": "upsellcomplaints-bar",
    "Unexpected Fees": "unexpectedfees-bar",
    "Vehicle Conditions": "vehicleconditions-bar",
    "Vehicle Cleanlines": "vehiclecleanlines-bar",
    "Long wait": "longwait-bar",
    "Long shuttle": "longshuttle-bar",
    "Shuttle Service": "shuttleservice-bar",
    "Location Complaint": "locationcomplaint-bar",
    "Geozone": "geozone-bar",
    "Damage Claims": "damageclaims-bar",
    "Rude service": "rudeservice-bar",
    "Unhelpful Service": "unhelpfulservice-bar",
    "Reserved Vehicle Unavailable": "reservedvehicleunavailable-bar",
    "Call Center Complaints": "callcentercomplaints-bar",
    "Deposit Hold": "depositissues-bar", 
    "Insurance Verification": "insuranceverification-bar",
    "Tolls and Violations": "tollsandviolations-bar",
    "Credit Check": "othercomplaints-bar", # Note: Credit Check was missing in CSS, defaulting to grey
    "Other Complaints": "othercomplaints-bar",
    "No Information": "noinformation-bar"
}


BULLET_CATEGORIES = [
    "Upsell complaints",
    "Vehicle Conditions",
    "Vehicle Cleanlines",
    "Rude service",
    "Reserved Vehicle Unavailable",
    "Shuttle Service"
]


def parse_complaint_dates(series, report_start, report_end):
    """Parse the CS database "Date of Complaint" column into real datetimes.

    The sheet stores the date as text without a year (e.g. "1-Sep", "28-Sep").
    pandas parses that as year 0001, so a 2026 weekly range never matches and
    every weekly number comes out as 0. Real datetimes pass through untouched;
    year-less values get the report year. A report week that crosses New Year
    (Dec -> Jan) assigns January dates to the end year.
    """
    import pandas as pd

    report_start = pd.Timestamp(report_start)
    report_end = pd.Timestamp(report_end)

    def _parse_one(value):
        if pd.isna(value):
            return pd.NaT
        if isinstance(value, pd.Timestamp):
            return value
        text = str(value).strip()
        parsed = pd.NaT
        for fmt in ("%d-%b-%Y", "%d-%b", "%d-%B", "%b-%d", "%B-%d", "%m/%d/%Y", "%m/%d", "%Y-%m-%d"):
            try:
                parsed = pd.to_datetime(text, format=fmt)
                break
            except (ValueError, TypeError):
                continue
        if parsed is pd.NaT:
            parsed = pd.to_datetime(text, errors="coerce")
        if parsed is pd.NaT or pd.isna(parsed):
            return pd.NaT
        # strptime without %Y yields 1900, pandas' fallback parser yields 0001;
        # either way a year before 2000 means the sheet gave no year at all.
        if parsed.year >= 2000:
            return parsed
        year = report_start.year
        if report_end.year != report_start.year and parsed.month <= report_end.month:
            year = report_end.year
        return parsed.replace(year=year)

    return series.map(_parse_one)
