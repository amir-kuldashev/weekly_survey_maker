from .context import context
from .const import locations

def count_yelp():
    default_yelp = []
    for loc in locations:
        location = {"name": loc, "d_pos": 0, "d_nr": 0, "d_neg": 0, "has_ace": True, "a_pos": 0, "a_nr": 0, "a_neg": 0}
        default_yelp.append(location)
    return default_yelp

def create_yelp():
    context["yelp_weekly_reviews"] = count_yelp()
    context["yelp_mtd_reviews"] = count_yelp()
