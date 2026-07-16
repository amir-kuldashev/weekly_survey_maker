import pandas as pd
from .context import context

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
            "res": row['R/A #'], 
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