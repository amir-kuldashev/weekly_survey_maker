import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import datetime
import json
import os

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".weekly_survey_maker.json")


def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_config(data):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except OSError:
        pass

def launch_gui(run_automation_callback, templates=None):
    """
    Builds and launches the Tkinter GUI.
    :param run_automation_callback: The function to call when 'Generate' is clicked.
    """
    root = tk.Tk()
    root.title("Drivo Report Automation")
    root.geometry("1300x800")
    root.configure(padx=20, pady=20)

    # Variables to store user inputs
    db_path_var = tk.StringVar()
    ra_path_var = tk.StringVar()
    refunds_path_var = tk.StringVar()
    start_date_var = tk.StringVar()
    end_date_var = tk.StringVar()
    month_var = tk.StringVar()
    output_path_var = tk.StringVar()
    templates = templates or {"Dashboard": "html_template_dashboard.html"}
    style_var = tk.StringVar(value=list(templates)[0])
    config = load_config()
    gemini_key_var = tk.StringVar(value=os.environ.get("GEMINI_API_KEY") or config.get("gemini_api_key", ""))

    # Style
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except tk.TclError:
        pass # Fallback to default if 'clam' isn't available

    # --- Button Action Functions ---
    def browse_db_file():
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        db_path_var.set(filepath)

    def browse_ra_file():
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        ra_path_var.set(filepath)

    def browse_refunds_file():
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        refunds_path_var.set(filepath)

    def browse_output_file():
        filepath = filedialog.asksaveasfilename(
            defaultextension=".html",
            initialfile="Finished_Report.html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            title="Save Report As",
        )
        if filepath:
            output_path_var.set(filepath)

    def on_generate_click():
        db_file = db_path_var.get()
        ra_file = ra_path_var.get()
        refunds_file = refunds_path_var.get()
        start = start_date_var.get()
        end = end_date_var.get()
        month = month_var.get()
        output_file = output_path_var.get()
        int_month = datetime.datetime.strptime(month, "%b").month
        # Basic Validation
        if not db_file or not ra_file or not refunds_file:
            messagebox.showwarning("Missing Files", "Please select all Excel files.")
            return
        if not start or not end or not month:
            messagebox.showwarning("Missing Dates", "Please fill out all date/month fields.")
            return
        if not output_file:
            messagebox.showwarning("Missing Output", "Please choose where to save the report.")
            return

        # Trigger the logic passed from main.py
        if run_automation_callback:
            template_name = templates.get(style_var.get(), list(templates.values())[0])
            gemini_key = gemini_key_var.get().strip()
            config["gemini_api_key"] = gemini_key
            save_config(config)
            saved_path = run_automation_callback(db_file, ra_file, refunds_file, start, end, int_month, output_file, template_name, gemini_key)
            from .context import context
            note = context.get("ai_specs_status") or ""
            messagebox.showinfo("Done", f"Report saved to:\n{saved_path or output_file}\n\nAI complaint specifications: {note}")
        else:
            messagebox.showinfo("Placeholder", "GUI working! Connect your logic function.")

    # --- UI Layout ---
    ttk.Label(root, text="Step 1: Upload Data", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))

    ttk.Label(root, text="Database File:").grid(row=1, column=0, sticky="w")
    ttk.Entry(root, textvariable=db_path_var, width=40).grid(row=1, column=1, padx=5)
    ttk.Button(root, text="Browse", command=browse_db_file).grid(row=1, column=2)

    ttk.Label(root, text="R/A File:").grid(row=2, column=0, sticky="w", pady=5)
    ttk.Entry(root, textvariable=ra_path_var, width=40).grid(row=2, column=1, padx=5, pady=5)
    ttk.Button(root, text="Browse", command=browse_ra_file).grid(row=2, column=2, pady=5)

    ttk.Label(root, text="Refunds File:").grid(row=3, column=0, sticky="w", pady=5)
    ttk.Entry(root, textvariable=refunds_path_var, width=40).grid(row=3, column=1, padx=5, pady=5)
    ttk.Button(root, text="Browse", command=browse_refunds_file).grid(row=3, column=2, pady=5)

    ttk.Label(root, text="Step 2: Set Dates", font=("Arial", 11, "bold")).grid(row=4, column=0, sticky="w", pady=(20, 10))

    ttk.Label(root, text="Week Start (YYYY-MM-DD):").grid(row=5, column=0, sticky="w")
    ttk.Entry(root, textvariable=start_date_var, width=15).grid(row=5, column=1, sticky="w", padx=5)

    ttk.Label(root, text="Week End (YYYY-MM-DD):").grid(row=6, column=0, sticky="w", pady=5)
    ttk.Entry(root, textvariable=end_date_var, width=15).grid(row=6, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(root, text="Report Month (e.g., Nov):").grid(row=7, column=0, sticky="w")
    month_combo = ttk.Combobox(root, textvariable=month_var, values=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], width=13)
    month_combo.grid(row=7, column=1, sticky="w", padx=5)

    ttk.Label(root, text="Gemini API key (optional, for complaint specifications):").grid(row=8, column=0, sticky="w", pady=(10, 0))
    ttk.Entry(root, textvariable=gemini_key_var, width=40, show="*").grid(row=8, column=1, padx=5, pady=(10, 0))

    ttk.Label(root, text="Step 3: Choose Output", font=("Arial", 11, "bold")).grid(row=9, column=0, sticky="w", pady=(20, 10))

    if len(templates) > 1:
        ttk.Label(root, text="Report Style:").grid(row=10, column=0, sticky="w")
        style_combo = ttk.Combobox(root, textvariable=style_var, values=list(templates), state="readonly", width=13)
        style_combo.grid(row=10, column=1, sticky="w", padx=5)

    ttk.Label(root, text="Save Report As:").grid(row=11, column=0, sticky="w", pady=5)
    ttk.Entry(root, textvariable=output_path_var, width=40).grid(row=11, column=1, padx=5, pady=5)
    ttk.Button(root, text="Browse", command=browse_output_file).grid(row=11, column=2, pady=5)

    # Generate Button
    generate_btn = ttk.Button(root, text="Generate HTML Report", command=on_generate_click)
    generate_btn.grid(row=12, column=0, columnspan=3, pady=25, ipadx=10, ipady=5)

    root.mainloop()
