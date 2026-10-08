import pandas as pd
from .context import context
from .const import normalize_location, safe_pct

def format_ra_number(value):
    """Show an R/A number as text: 'EWRCON-1006' stays as is, a numeric id that
    pandas read as a float (123456.0) is shown as 123456, blanks become ''."""
    if value is None or (isinstance(value, float) and pd.isna(value)) or value is pd.NA:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def create_refunds(refunds_file):
    context["total_refunds"] = f"${-float((refunds_file['Amount'].iloc[-1]))}"
    refunds_file = refunds_file[:-1]
    refunds_list = []
    for _, row in refunds_file.iterrows():
        raw_date = row['Charge Date']  # pandas parses this into a Timestamp on read
        date_obj = pd.to_datetime(raw_date)
        short_date = f"{date_obj.month}/{date_obj.day}/{date_obj.year}"
        month_year = date_obj.strftime('%B %Y')
        
        location = {
            "res": format_ra_number(row['R/A #']), 
            "loc": row['Unnamed: 0'], 
            "month": month_year, 
            "date": short_date, 
            "amount": f"$({-(float(row['Amount']))})", 
            "agent": "", 
            "dept": "CREDIT-CS", 
            "notes": ""
        }
        refunds_list.append(location)
    context["refunds_list"] = refunds_list

    # Per-location summary (the dashboard report shows this instead of each contract).
    total_amount = float(-refunds_file['Amount'].sum()) if len(refunds_file) else 0.0
    by_location = []
    grouped = refunds_file.assign(_loc=refunds_file['Unnamed: 0'].map(normalize_location)).groupby('_loc', dropna=False)
    for loc, rows in grouped:
        amount = float(-rows['Amount'].sum())
        by_location.append({
            "loc": loc if isinstance(loc, str) else "Unknown",
            "count": int(len(rows)),
            "amount": f"${amount:,.2f}",
            "amount_value": amount,
            "pct": safe_pct(amount, total_amount),
        })
    by_location.sort(key=lambda r: r["amount_value"], reverse=True)
    context["refunds_by_location"] = by_location
    context["refunds_count"] = int(len(refunds_file))