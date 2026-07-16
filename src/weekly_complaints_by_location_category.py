from .context import context
from .const import locations, ALL_COMPLAINTS, BULLET_CATEGORIES,CATEGORY_STYLES

def count_category_by_location(weekly_data):
    weekly_data_non_duplicate = weekly_data[weekly_data["Duplicate?"] == "No"]
    drivo_survey_cc = weekly_data_non_duplicate[(weekly_data_non_duplicate["Source"] == "Drivo Survey") 
                                                | (weekly_data_non_duplicate["Source"] == "Call Center")]
    location_chart_data = []
    narrative_lists = []
    
    for loc in locations:
        loc_data = drivo_survey_cc[drivo_survey_cc["Location"] == loc]
        total_complaints = (loc_data[ALL_COMPLAINTS] == "Yes").sum().sum()
        location = {
            "name": loc,
            "total_complaints": total_complaints,
            "categories": [
                
            ]
        }
        loc_surveys = loc_data[loc_data["Source"] == "Drivo Survey"]
        negative_surveys_count = (loc_surveys["Stars"] == 1).sum() + (loc_surveys["Stars"] == 2).sum()
        cc_feedback = (loc_data["Source"] == "Call Center").sum()
        
        narrative_location = {
            "name": loc,
            "negative_surveys": negative_surveys_count,
            "cc_feedback": cc_feedback,
            "total_complaints": total_complaints,
            "bullets": []
        }
        
        other_bullet = {"count": total_complaints-(loc_data[BULLET_CATEGORIES] == "Yes").sum().sum(), "title": "other complaints", "description": 'Various issues.'}
        narrative_location["bullets"].append(other_bullet)
        
        for complaint in ALL_COMPLAINTS:
            category_count = (loc_data[complaint] == "Yes").sum()
            if category_count == 0:
                continue
            category = {"name": complaint, "css_class": CATEGORY_STYLES.get(complaint, "othercomplaints-bar"), "percentage": category_count/total_complaints*100, "count": category_count}
            location["categories"].append(category)
            if complaint in BULLET_CATEGORIES:
                bullet = {"count": category_count, "title": complaint, "description": ''}
                narrative_location["bullets"].append(bullet)
               
        
        location_chart_data.append(location)
        narrative_lists.append(narrative_location)
    
    call_center_complaints_block = {
            "name": "Call Center",
            "negative_surveys": (drivo_survey_cc["Call Center Complaints"] == "Yes").sum(),
            "cc_feedback": 0,
            "total_complaints": (drivo_survey_cc["Call Center Complaints"] == "Yes").sum(),
            "bullets": [{"count": category_count, "title": "unhelpful", "description": ''}]
        }


    narrative_lists.append(call_center_complaints_block)
    context["location_chart_data"] = location_chart_data
    context["narrative_lists"] = narrative_lists
