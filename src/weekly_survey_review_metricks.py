from .context import context
from .const import locations
review_sources = ["GOOGLE","YELP","TRUSTPILOT"]

def create_surveys(weekly_file):
    surveys_file = weekly_file[weekly_file["Source"]=="Drivo Survey"]
    surveys_file_non_duplicate = surveys_file[surveys_file["Duplicate?"] == "No"]
    stars_count = surveys_file_non_duplicate["Stars"].value_counts()
    
    context["surveys_total"] = stars_count.sum()
    context["surveys_pos_count"] = stars_count.get(5,0)+stars_count.get(4,0)
    context["surveys_neutral_count"] = stars_count.get(3,0)
    context["surveys_nodesc_count"] = (surveys_file_non_duplicate["No Information"]=="Yes").sum()
    context["surveys_neg_count"] = stars_count.get(2,0) + stars_count.get(1,0)-context["surveys_nodesc_count"]
    
def create_reviews(weekly_file):
    reviews_file = weekly_file[weekly_file["Source"].isin(["GOOGLE", "YELP", "TRUSTPILOT"])]
    stars_count = reviews_file["Stars"].value_counts()
    
    # Among all Brands
    context["reviews_total"] = stars_count.sum()
    context["reviews_nodesc_count"] = (reviews_file["No Information"] == "Yes").sum()
    context["reviews_pos_count"] = stars_count.get(5,0)+stars_count.get(4,0)
    context["reviews_neutral_count"] = stars_count.get(3,0)
    context["reviews_neg_count"] = stars_count.get(1,0)+stars_count.get(2,0)-context["reviews_nodesc_count"]
    
    #Drivo Brand
    drivo_reviews_file = reviews_file[reviews_file["Brand"]=="Drivo"]
    source_count = drivo_reviews_file["Source"].value_counts()
    context["drivo_reviews_total"] = source_count.sum()
    
    for source in review_sources:
        context[f"drivo_{source.lower()}_count"] = source_count.get(source,0)
        context[f"drivo_{source.lower()}_pct"] = context[f"drivo_{source.lower()}_count"]/context["drivo_reviews_total"]*100
        
    #Ace Brand
    ace_reviews_file = reviews_file[reviews_file["Brand"]=="ACE"]
    source_count = ace_reviews_file["Source"].value_counts()
    context["ace_reviews_total"] = source_count.sum()
    
    for source in review_sources:
        context[f"ace_{source.lower()}_count"] = source_count.get(source,0)
        context[f"ace_{source.lower()}_pct"] = context[f"ace_{source.lower()}_count"]/context["ace_reviews_total"]*100

    
def cc_complains(weekly_file):
    call_center_file = weekly_file[weekly_file["Source"] == "Call Center"]
    call_center_count = call_center_file["Location"].value_counts()

    context["cc_total"] = call_center_count.sum()
    for loc in locations:
        context[f"cc_{loc.lower()}"] = call_center_count.get(loc,0)

def confirmed_cases(weekly_file):
    weekly_file_non_duplicate = weekly_file[weekly_file["Duplicate?"]=="No"]
    confirmed_file = weekly_file_non_duplicate[weekly_file_non_duplicate["Confirmed "] == "Y"]

    confirmed_cases_list =[]
    
    for index, row in confirmed_file.iterrows():
        confirmed_cases_list.append({
            "id" : row.get("R/A OR CONFIRMATION","Unknown"),
            "description": row.get("Investigation Result","Unknown")
        })
    context["confirmed_cases"] = confirmed_cases_list
    
def create_weekly_survey_review__metrciks(weekly_file):
    create_surveys(weekly_file)
    create_reviews(weekly_file)
    cc_complains(weekly_file)
    confirmed_cases(weekly_file)