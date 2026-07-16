from .context import context
from .const import ALL_COMPLAINTS

# range can either be mtd or weekly
def count_total_complaints(complaints, range):
    breakdown_rows = []
    
    for complaint in ALL_COMPLAINTS:
        count = (complaints[complaint] == "Yes").sum()
        pct_total = (float(count)/float(context[f"{range}_total_complaints"]))*100
        pct_ra = (float(count)/float(context[f"{range}_closed_ras"]))*100
        row = {"category": complaint, 
               "cases": count, 
               "pct_total": f"{pct_total:.2f}", 
               "pct_ra": f"{pct_ra:.2f}"
               }
        breakdown_rows.append(row)
    breakdown_rows.sort(key=lambda x: x["cases"], reverse=True)
    return breakdown_rows


def weekly_vs_mtd_breakdown(weekly_complaints_file, monthly_complaints_file, weekly_RA_file):
    
    weekly_survey_cc = weekly_complaints_file[(weekly_complaints_file["Source"]=="Drivo Survey") | (weekly_complaints_file["Source"]=="Call Center")]
    weekly_non_duplicate = weekly_survey_cc[weekly_survey_cc["Duplicate?"]=="No"]
    monthly_survey_cc = monthly_complaints_file[(monthly_complaints_file["Source"]=="Drivo Survey") | (monthly_complaints_file["Source"]=="Call Center")]
    monthly_non_duplicate = monthly_survey_cc[monthly_survey_cc["Duplicate?"]=="No"]
    
    context["weekly_total_complaints"] = (weekly_non_duplicate[ALL_COMPLAINTS]== "Yes").sum().sum()
    context["mtd_total_complaints"] = (monthly_non_duplicate[ALL_COMPLAINTS] == "Yes").sum().sum()
    context["weekly_closed_ras"] = len(weekly_RA_file)
    context["weekly_breakdown_rows"] = count_total_complaints(weekly_non_duplicate,"weekly")
    context["mtd_breakdown_rows"] = count_total_complaints(monthly_non_duplicate,"mtd")
