from context import context
def calculate_ratios(complaints, range): 
    complaints_surveys_cc = complaints[(complaints["Source"] == "Call Center") | (complaints["Source"] == "Drivo Survey")]
    non_duplicate = complaints_surveys_cc[complaints_surveys_cc["Duplicate?"]=="No"]
    
    context[f"{range}_all_complaints"] = (non_duplicate["Stars"] == 1).sum()+(non_duplicate["Stars"] == 2).sum()
    context[f"{range}_ratio_all"] = round(context[f"{range}_all_complaints"]/context[f"{range}_closed_ras"]*100,2)
    
    context[f"{range}_survey_cc_only"] = context[f"{range}_all_complaints"] - (non_duplicate["No Information"] == "Yes").sum()
    context[f"{range}_ratio_survey_cc"] = round(context[f"{range}_survey_cc_only"]/context[f"{range}_closed_ras"]*100,2)
    
    
def create_ratios(weekly_complaints,monthly_complaints):
    calculate_ratios(weekly_complaints, "weekly")
    calculate_ratios(monthly_complaints, "mtd")