import os
import sys
import pandas as pd
from jinja2 import Environment, FileSystemLoader


def resource_path(relative_path):
    """Resolve a bundled resource path in both dev and PyInstaller builds.

    When frozen, PyInstaller extracts data files to sys._MEIPASS; in dev we
    fall back to the current working directory.
    """
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)
from .context import context
from .first_block import create_first_block
from .weekly_survey_review_metricks import create_weekly_survey_review__metrciks
from .weekly_complaints_by_location_category import count_category_by_location
from .weekly_vs_mtd_breakdown import weekly_vs_mtd_breakdown
from .ratios import create_ratios
from .survey_metricks import calculate_survey_metricks
from .google_reviews import create_google_reviews
from .yelp import create_yelp
from .bbb import create_BBB
from .nps import create_nps
from .refunds import create_refunds
from .const import normalize_location

def generate_full_report(db_file, ra_file, refunds_path,start, end, int_month, output_path=None):
    complaints_file = pd.read_excel(db_file)
    RA_file = pd.read_excel(ra_file)
    refunds_file = pd.read_excel(refunds_path)
    # Normalize location codes (strip/upper) so they match the codes in const.locations.
    complaints_file["Location"] = complaints_file["Location"].map(normalize_location)
    RA_file["Pickup Location"] = RA_file["Pickup Location"].map(normalize_location)
    # Excel exports sometimes store dates as text; make sure both date columns
    # are real datetimes so the .dt accessor and range filters work.
    complaints_file["Date of Complaint"] = pd.to_datetime(complaints_file["Date of Complaint"], errors="coerce")
    RA_file["Drop Off Date"] = pd.to_datetime(RA_file["Drop Off Date"], errors="coerce")
    month = int_month

    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)
    sent_dt = end_dt + pd.Timedelta(days=2)

    weekly_complaints_file = complaints_file[(complaints_file['Date of Complaint'] >= start_dt) & (complaints_file['Date of Complaint'] <= end_dt)]
    monthly_complaints_file = complaints_file[complaints_file["Date of Complaint"].dt.month == month]

    # end of week should be +1 day for the R/A file
    weekly_RA_file = RA_file[(RA_file['Drop Off Date'] >= start_dt) & (RA_file['Drop Off Date'] <= end_dt+pd.Timedelta(days=1))]
    print(len(weekly_RA_file))
    monthly_RA_file = RA_file[RA_file['Drop Off Date'].dt.month == month]
    print(len(monthly_RA_file))
    
    
    context["report_week_date_range"] = f"{start_dt.strftime('%b %-d')} - {end_dt.strftime('%b %-d')}"
    context["sent_date"] = f"{sent_dt.strftime('%b %-d')}"
    
    month_start_dt = pd.Timestamp(year=start_dt.year, month=month, day=1)
    month_end_date = month_start_dt + pd.offsets.MonthEnd(0)
    mtd_end_dt = min(end_dt, month_end_date)
    
    context["mtd_date_range"] = f"{month_start_dt.strftime('%-m/%-d')} - {mtd_end_dt.strftime('%-m/%-d')}"
    context["weekly_date_range"] = f"{start_dt.strftime('%-m/%-d')} - {end_dt.strftime('%-m/%-d')}"
       
    def run_all_blocks():
        create_first_block(monthly_complaints_file,monthly_RA_file)
        create_weekly_survey_review__metrciks(weekly_complaints_file)
        count_category_by_location(weekly_complaints_file)
        weekly_vs_mtd_breakdown(weekly_complaints_file, monthly_complaints_file, weekly_RA_file)
        create_ratios(weekly_complaints_file, monthly_complaints_file)
        calculate_survey_metricks(weekly_complaints_file, monthly_complaints_file, weekly_RA_file,monthly_RA_file)
        create_google_reviews(weekly_complaints_file,monthly_complaints_file)
        create_yelp()
        create_BBB(weekly_complaints_file,monthly_complaints_file)
        create_nps()
        create_refunds(refunds_file)
        
    run_all_blocks()
    env = Environment(loader=FileSystemLoader(resource_path('.')))
    template = env.get_template("html_template.html")
    rendered_html = template.render(context)
    
    output_filename = output_path or "Finished_Report.html"
    with open(output_filename,"w", encoding="utf-8") as f:
        f.write(rendered_html)
    return output_filename