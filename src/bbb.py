from context import context
from const import locations

def count_BBB(reviews):
    bbb_reviews = []
    
    for loc in locations:
        bbb_loc = reviews[reviews["Location"] == loc]
        bbb_loc_count = bbb_loc["Stars"].value_counts()
        
        location = {"name": loc, 
                    "pos": bbb_loc_count.get(5,0)+bbb_loc_count.get(4,0),
                    "neg": bbb_loc_count.get(3,0)+bbb_loc_count.get(2,0)+bbb_loc_count.get(1,0)
                    }
        bbb_reviews.append(location)
    
    return bbb_reviews

def create_BBB(weekly_complaints_file, monthly_complaints_file):
    weekly_BBB = weekly_complaints_file[weekly_complaints_file["Source"] == "BBB"]  
    monthly_BBB = monthly_complaints_file[monthly_complaints_file["Source"] == "BBB"]  
    context["bbb_reviews_weekly"] = count_BBB(weekly_BBB)
    context["bbb_reviews_mtd"] = count_BBB(monthly_BBB)
    