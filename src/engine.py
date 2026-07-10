import pandas as pd
from jinja2 import Environment, FileSystemLoader
from context import context
from first_block import create_first_block
from weekly_survey_review_metricks import create_weekly_survey_review__metrciks
from weekly_complaints_by_location_category import count_category_by_location
from weekly_vs_mtd_breakdown import weekly_vs_mtd_breakdown
from ratios import create_ratios
from survey_metricks import calculate_survey_metricks
from google_reviews import create_google_reviews
from yelp import create_yelp
from bbb import create_BBB
from nps import create_nps

def generate_full_report():
    complaints_file = pd.read_excel("example_data.xlsx")
    RA_file = pd.read_excel("RAReporting.xlsx")
    
    start_of_week = '2026-06-29'
    # end of week should be +1 day
    end_of_week = '2026-07-05'
    month = 6
    
    weekly_complaints_file = complaints_file[(complaints_file['Date of Complaint'] >= start_of_week) & (complaints_file['Date of Complaint'] <= end_of_week)]
    monthly_complaints_file = complaints_file[complaints_file["Date of Complaint"].dt.month == month]
    
    
    start_dt = pd.to_datetime(start_of_week)
    end_dt = pd.to_datetime(end_of_week)
    sent_dt = end_dt + pd.Timedelta(days=2)
    
    weekly_RA_file = RA_file[(RA_file['Drop Off Date'] >= start_of_week) & (RA_file['Drop Off Date'] <= end_dt+pd.Timedelta(days=1))]
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
   
    
    
    run_all_blocks(weekly_complaints_file,monthly_complaints_file,weekly_RA_file,monthly_RA_file)
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("html_template.html")
    rendered_html = template.render(context)
    
    output_filename = "Finished_Report.html"
    with open(output_filename,"w", encoding="utf-8") as f:
        f.write(rendered_html)
        
def run_all_blocks(weekly_complaints_file,monthly_complaints_file,weekly_RA_file,monthly_RA_file):
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
generate_full_report()