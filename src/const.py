locations = ["EWR", "EWRCON", "JFK", "LGA", "BRK", "BRKJS"]


def normalize_location(value):
    """Clean a raw location code from the R/A export or CS database.

    Codes are stripped and upper-cased so e.g. " ewrcon" matches "EWRCON".
    Every code is reported as its own location (EWRCON is NOT folded into EWR).
    """
    if not isinstance(value, str):
        return value
    return value.strip().upper()


def safe_pct(numerator, denominator, digits=2):
    """Percentage that returns 0 instead of raising when the denominator is 0.

    Small locations (e.g. EWRCON) can have no closed R/As in a given week.
    """
    if not denominator:
        return 0
    return round(float(numerator) / float(denominator) * 100, digits)

ALL_COMPLAINTS = [
    "Upsell complaints",
    "Unexpected Fees",
    "Vehicle Conditions",
    "Vehicle Cleanlines",
    "Long wait",
    "Long shuttle",
    "Shuttle Service",
    "Location Complaint",
    "Geozone",
    "Damage Claims",
    "Rude service",
    "Unhelpful Service",
    "Reserved Vehicle Unavailable",
    "Call Center Complaints",
    "Deposit Hold",
    "Insurance Verification",
    "Tolls and Violations",
    "Credit Check",
    "Other Complaints",
    "No Information"
]

CATEGORY_STYLES = {
    "Upsell complaints": "upsellcomplaints-bar",
    "Unexpected Fees": "unexpectedfees-bar",
    "Vehicle Conditions": "vehicleconditions-bar",
    "Vehicle Cleanlines": "vehiclecleanlines-bar",
    "Long wait": "longwait-bar",
    "Long shuttle": "longshuttle-bar",
    "Shuttle Service": "shuttleservice-bar",
    "Location Complaint": "locationcomplaint-bar",
    "Geozone": "geozone-bar",
    "Damage Claims": "damageclaims-bar",
    "Rude service": "rudeservice-bar",
    "Unhelpful Service": "unhelpfulservice-bar",
    "Reserved Vehicle Unavailable": "reservedvehicleunavailable-bar",
    "Call Center Complaints": "callcentercomplaints-bar",
    "Deposit Hold": "depositissues-bar", 
    "Insurance Verification": "insuranceverification-bar",
    "Tolls and Violations": "tollsandviolations-bar",
    "Credit Check": "othercomplaints-bar", # Note: Credit Check was missing in CSS, defaulting to grey
    "Other Complaints": "othercomplaints-bar",
    "No Information": "noinformation-bar"
}


BULLET_CATEGORIES = [
    "Upsell complaints",
    "Vehicle Conditions",
    "Vehicle Cleanlines",
    "Rude service",
    "Reserved Vehicle Unavailable",
    "Shuttle Service"
]
