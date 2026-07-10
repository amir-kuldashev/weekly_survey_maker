import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def launch_gui(run_automation_callback):
    """
    Builds and launches the Tkinter GUI.
    :param run_automation_callback: The function to call when 'Generate' is clicked.
    """
    root = tk.Tk()
    root.title("Drivo Report Automation")
    root.geometry("550x380")
    root.configure(padx=20, pady=20)

    # Variables to store user inputs
    db_path_var = tk.StringVar()
    ra_path_var = tk.StringVar()
    start_date_var = tk.StringVar()
    end_date_var = tk.StringVar()
    month_var = tk.StringVar()

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

    def on_generate_click():
        db_file = db_path_var.get()
        ra_file = ra_path_var.get()
        start = start_date_var.get()
        end = end_date_var.get()
        month = month_var.get()
        
        # Basic Validation
        if not db_file or not ra_file:
            messagebox.showwarning("Missing Files", "Please select both Excel files.")
            return
        if not start or not end or not month:
            messagebox.showwarning("Missing Dates", "Please fill out all date/month fields.")
            return
            
        # Trigger the logic passed from main.py
        if run_automation_callback:
            run_automation_callback(db_file, ra_file, start, end, month)
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

    ttk.Label(root, text="Step 2: Set Dates", font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=(20, 10))

    ttk.Label(root, text="Week Start (YYYY-MM-DD):").grid(row=4, column=0, sticky="w")
    ttk.Entry(root, textvariable=start_date_var, width=15).grid(row=4, column=1, sticky="w", padx=5)

    ttk.Label(root, text="Week End (YYYY-MM-DD):").grid(row=5, column=0, sticky="w", pady=5)
    ttk.Entry(root, textvariable=end_date_var, width=15).grid(row=5, column=1, sticky="w", padx=5, pady=5)

    ttk.Label(root, text="Report Month (e.g., Nov):").grid(row=6, column=0, sticky="w")
    month_combo = ttk.Combobox(root, textvariable=month_var, values=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], width=13)
    month_combo.grid(row=6, column=1, sticky="w", padx=5)

    # Generate Button
    generate_btn = ttk.Button(root, text="Generate HTML Report", command=on_generate_click)
    generate_btn.grid(row=7, column=0, columnspan=3, pady=25, ipadx=10, ipady=5)

    root.mainloop()

# Optional: Allows you to run just the GUI file directly to test the visuals
if __name__ == "__main__":
    launch_gui(None)