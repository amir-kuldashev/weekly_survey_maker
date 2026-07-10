context = {
    # --- Header Information ---
    "report_week_date_range": -1,
    "sent_date": -1,

    # --- MTD Overall Table ---
    "mtd_overall_neg_complaints": -1,
    "mtd_closed_ras": -1,
    "mtd_overall_ratio": -1,
    
    "mtd_ewr_complaints": -1,
    "mtd_ewr_ras": -1,
    "mtd_ewr_pct": -1,
    
    "mtd_jfk_complaints": -1,
    "mtd_jfk_ras": -1,
    "mtd_jfk_pct": -1,
    
    "mtd_lga_complaints": -1,
    "mtd_lga_ras": -1,
    "mtd_lga_pct": -1,
    
    "mtd_brk_complaints": -1,
    "mtd_brk_ras": -1,
    "mtd_brk_pct": -1,
    
    "mtd_brkjs_complaints": -1,
    "mtd_brkjs_ras": -1,
    "mtd_brkjs_pct": -1,

    # --- KPI Cards (Surveys & Reviews) ---
    "surveys_total": -1,
    "surveys_pos_count": -1,
    "surveys_neg_count": -1,
    "surveys_nodesc_count": -1,
    "surveys_neutral_count": -1,

    "reviews_total": -1,
    "reviews_pos_count": -1,
    "reviews_neg_count": -1,
    "reviews_nodesc_count": -1,
    "reviews_neutral_count": -1,

    # --- Review Sources (Drivo) ---
    "drivo_reviews_total": -1,
    "drivo_google_pct": -1,
    "drivo_google_count": -1,
    "drivo_yelp_pct": -1,
    "drivo_yelp_count": -1,
    "drivo_trustpilot_pct": -1,
    "drivo_trustpilot_count": -1,

    # --- Review Sources (Ace) ---
    "ace_reviews_total": -1,
    "ace_google_pct": -1,
    "ace_google_count": -1,
    "ace_yelp_pct": -1,
    "ace_yelp_count": -1,
    "ace_trustpilot_pct": -1,
    "ace_trustpilot_count": -1,

    # --- Call Center Complaints ---
    "cc_jfk": -1,
    "cc_ewr": -1,
    "cc_brk": -1,
    "cc_brkjs": -1,
    "cc_lga": -1,
    "cc_total": -1,

    # --- Confirmed Cases Loop ---
    "confirmed_cases": [
        {"id": -1, "description": -1}
    ],

    # --- Location & Category Chart Loop ---
    "location_chart_data": [
        {
            "name": -1,
            "total_complaints": -1,
            "categories": [
                {"name": -1, "css_class": "othercomplaints-bar", "percentage": -1, "count": -1}
            ]
        }
    ],

    # --- Narrative Lists Loop ---
    "narrative_lists": [
        {
            "name": -1,
            "negative_surveys": -1,
            "cc_feedback": -1,
            "total_complaints": -1,
            "bullets": [
                {"count": -1, "title": -1, "description": -1}
            ]
        }
    ],

    # --- Weekly vs MTD Breakdown ---
    "weekly_total_complaints": -1,
    "weekly_closed_ras": -1,
    "mtd_date_range": -1,
    "mtd_total_complaints": -1,

    "weekly_breakdown_rows": [
        {"category": -1, "cases": -1, "pct_total": -1, "pct_ra": -1}
    ],
    
    "mtd_breakdown_rows": [
        {"category": -1, "cases": -1, "pct_total": -1, "pct_ra": -1}
    ],

    # --- Ratios Tables ---
    "weekly_date_range": -1,
    "weekly_survey_cc_only": -1,
    "weekly_ratio_survey_cc": -1,
    "weekly_all_complaints": -1,
    "weekly_ratio_all": -1,

    "mtd_survey_cc_only": -1,
    "mtd_ratio_survey_cc": -1,
    "mtd_all_complaints": -1,
    "mtd_ratio_all": -1,

    # --- Email Survey Metrics ---
    "email_total_sent": -1,
    "email_total_target": -1,
    "email_total_pct": -1,
    
    "email_survey_locations": [
        {"name": -1, "sent": -1, "target": -1, "pct": -1}
    ],
    
   "survey_metrics": [
        {
            "name": "Placeholder",
            "weekly": {
                "pos": -1, 
                "neg": -1, 
                "neutral": -1, 
                "sent": -1, 
                "target": -1, 
                "pct": -1
            },
            "mtd": {
                "pos": -1, 
                "neg": -1, 
                "neutral": -1, 
                "sent": -1, 
                "target": -1, 
                "pct": -1
            }
        }
    ],

    # --- Google Reviews ---
    "google_weekly_reviews": [
        {"name": -1, "d_pos": -1, "d_neg": -1, "a_pos": -1, "a_neg": -1}
    ],
    "google_mtd_reviews": [
        {"name": -1, "d_pos": -1, "d_neg": -1, "a_pos": -1, "a_neg": -1}
    ],

    # --- Yelp Reviews ---
    "yelp_weekly_reviews": [
        {"name": -1, "d_pos": -1, "d_nr": -1, "d_neg": -1, "has_ace": True, "a_pos": -1, "a_nr": -1, "a_neg": -1}
    ],
    "yelp_mtd_reviews": [
        {"name": -1, "d_pos": -1, "d_nr": -1, "d_neg": -1, "has_ace": True, "a_pos": -1, "a_nr": -1, "a_neg": -1}
    ],

    # --- BBB Reviews ---
    "bbb_reviews_weekly": [
        {"name": -1, "pos": -1, "neg": -1}
    ],
    "bbb_reviews_mtd": [
        {"name": -1, "pos": -1, "neg": -1}
    ],


    # --- NPS Scores ---
    "nps_weekly_total": -1,
    "nps_weekly_locations": [
        {"name": -1, "score": -1}
    ],
    
    "nps_mtd_total": -1,
    "nps_mtd_locations": [
        {"name": -1, "score": -1}
    ],

    # --- Refunds Table ---
    "total_refunds": -1,
    "refunds_list": [
        {
            "res": -1, 
            "loc": -1, 
            "month": -1, 
            "date": -1, 
            "amount": -1, 
            "agent": -1, 
            "dept": -1, 
            "notes": -1
        }
    ]
}