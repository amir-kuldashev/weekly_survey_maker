from .const import locations
from .context import context



def count_google_reviews(reviews):
    google_reviews = []
    for loc in locations:
        loc_data = reviews[reviews["Location"] == loc]
        drivo_loc_data = loc_data[loc_data["Brand"]=="Drivo"]
        ace_loc_data = loc_data[loc_data["Brand"]=="ACE"]
        drivo_loc_count = drivo_loc_data["Stars"].value_counts()
        ace_loc_count = ace_loc_data["Stars"].value_counts()
        location = {"name": loc, 
                    "d_pos": drivo_loc_count.get(5,0)+drivo_loc_count.get(4,0), 
                    "d_neg": drivo_loc_count.get(1,0)+drivo_loc_count.get(2,0)+drivo_loc_count.get(3,0), 
                    "a_pos": ace_loc_count.get(5,0)+ace_loc_count.get(4,0), 
                    "a_neg": ace_loc_count.get(1,0)+ace_loc_count.get(2,0)+ace_loc_count.get(3,0)
                    }
        google_reviews.append(location)
    
    return google_reviews 

def create_google_reviews(weekly_complaints_file, monthly_complaints_file):
    weekly_google = weekly_complaints_file[weekly_complaints_file["Source"] == "GOOGLE"]  
    monthly_google = monthly_complaints_file[monthly_complaints_file["Source"] == "GOOGLE"]  
    context["google_weekly_reviews"] = count_google_reviews(weekly_google)
    context["google_mtd_reviews"] = count_google_reviews(monthly_google)
    