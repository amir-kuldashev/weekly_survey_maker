from .const import locations
from .context import context

def calculate_survey_metricks(weekly_complaints, monthly_complaints, weekly_RA,monthly_RA):
    weekly_surveys = weekly_complaints[weekly_complaints["Source"] == "Drivo Survey"]
    weekly_non_duplicate = weekly_surveys[weekly_surveys["Duplicate?"] == "No"]
    monthly_surveys = monthly_complaints[monthly_complaints["Source"] == "Drivo Survey"]
    monthly_non_duplicate = monthly_surveys[monthly_surveys["Duplicate?"] == "No"]
    
    context["email_total_sent"] = len(weekly_non_duplicate)
    context["email_total_target"] = len(weekly_RA)
    context["email_total_pct"] = round(context["email_total_sent"]/context["email_total_target"]*100,2)
    
    surveys_weekly_loc_count = weekly_non_duplicate["Location"].value_counts()
    surveys_monthly_loc_count = monthly_non_duplicate["Location"].value_counts()
    
    RA_weekly_loc_count = weekly_RA["Pickup Location"].value_counts()
    RA_monthly_loc_count = monthly_RA["Pickup Location"].value_counts()
    email_survey_locations = []
    
    for loc in locations:
        
        row = {"name": loc, 
               "sent": surveys_weekly_loc_count.get(loc,0), 
               "target": RA_weekly_loc_count.get(loc,0), 
               "pct": -1}

        row["pct"] = round(row["sent"]/row["target"]*100,2)
        
        email_survey_locations.append(row)

    context["email_survey_locations"] = email_survey_locations
    
    # Weekly and MTD
    
    survey_metrics = []
    
    for loc in locations:
        
        loc_weekly_data = weekly_non_duplicate[weekly_non_duplicate["Location"] == loc]
        loc_monthly_data = monthly_non_duplicate[monthly_non_duplicate["Location"] == loc]
        loc_weekly_count = loc_weekly_data["Stars"].value_counts() 
        loc_monthly_count = loc_monthly_data["Stars"].value_counts()
        
        location = {
            "name": loc,
            "weekly": {
                "pos": loc_weekly_count.get(5,0)+loc_weekly_count.get(4,0), 
                "neg": loc_weekly_count.get(1,0) + loc_weekly_count.get(2,0), 
                "neutral": loc_weekly_count.get(3,0), 
                "sent": surveys_weekly_loc_count.get(loc,0), 
                "target": RA_weekly_loc_count.get(loc,0), 
                "pct": round(surveys_weekly_loc_count.get(loc,0)/RA_weekly_loc_count.get(loc,0)*100,2)
            },
            "mtd": {
                "pos": loc_monthly_count.get(5,0)+loc_monthly_count.get(4,0), 
                "neg": loc_monthly_count.get(1,0)+loc_monthly_count.get(2,0), 
                "neutral": loc_monthly_count.get(3,0), 
                "sent": surveys_monthly_loc_count.get(loc,0), 
                "target": RA_monthly_loc_count.get(loc,0), 
                "pct": round(surveys_monthly_loc_count.get(loc,0)/RA_monthly_loc_count.get(loc,0)*100,2)
            }
        }
        survey_metrics.append(location)
    
    context["survey_metrics"] = survey_metrics