from .context import context
from .const import locations

def count_nps():
    default_nps = []
    for loc in locations:
        location = {"name": loc, "score": 0}
        default_nps.append(location)
    return default_nps

def create_nps():
    context["nps_weekly_total"] = 0
    context["nps_mtd_total"] = 0
    context["nps_weekly_locations"] = count_nps()
    context["nps_mtd_locations"] = count_nps()