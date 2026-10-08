from .context import context
import pandas as pd
from .const import locations, safe_pct

def count_by_brand(data, complaint_columns):
    """Split a complaint count into Drivo / Ace using the CS database Brand column."""
    brand = data["Brand"].astype(str).str.strip().str.upper()
    return {
        "drivo": int((data.loc[brand == "DRIVO", complaint_columns] == "Yes").sum().sum()),
        "ace": int((data.loc[brand == "ACE", complaint_columns] == "Yes").sum().sum()),
    }


def count_controllable_complaints(file):
    
    controllable_complains = ['Reserved Vehicle Unavailable',
                              'Long shuttle','Long wait','Rude service','Shuttle Service',
                              'Unexpected Fees','Unhelpful Service','Upsell complaints',
                              'Vehicle Conditions','Vehicle Cleanlines']
    
    non_duplicate_data = file[file['Duplicate?'] == 'No']
    mtd_overall_neg_complaints = (non_duplicate_data[controllable_complains] == 'Yes').sum().sum()
    context["mtd_overall_neg_complaints"] = mtd_overall_neg_complaints
    context["mtd_overall_neg_by_brand"] = count_by_brand(non_duplicate_data, controllable_complains)
    
    for loc in locations:
        loc_data = non_duplicate_data[non_duplicate_data["Location"] == loc]
        
        # Calculate complaints
        complaint_count = (loc_data[controllable_complains] == "Yes").sum().sum()
        
        # Dynamically assign to context
        # This creates keys like mtd_ewr_complaints, mtd_jfk_complaints, etc.
        key_name = f"mtd_{loc.lower()}_complaints"
        context[key_name] = complaint_count


def count_monthly_RA(file):
    location_counts = file['Pickup Location'].value_counts()
    context["mtd_closed_ras"] = location_counts.sum()
    
    for loc in locations:
        loc_total = location_counts.get(loc, 0)
        context[f"mtd_{loc.lower()}_ras"] = loc_total


def count_monthly_pct():
    context["mtd_overall_ratio"] = safe_pct(context["mtd_overall_neg_complaints"], context["mtd_closed_ras"])
    for loc in locations:
        context[f"mtd_{loc.lower()}_pct"] = safe_pct(context[f"mtd_{loc.lower()}_complaints"], context[f"mtd_{loc.lower()}_ras"])

def create_first_block(complaints_file, RA_file):
    count_controllable_complaints(complaints_file)
    count_monthly_RA(RA_file)
    count_monthly_pct()



if __name__ == "__main__":
    complaints_file = pd.read_excel("example_data.xlsx")
    RA_file = pd.read_excel("RAReporting.xlsx")
    create_first_block(complaints_file, RA_file)