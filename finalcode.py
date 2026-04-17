# ============================================================
# RTT DEVICE TRACKER PRO (FINAL INDUSTRY VERSION)
# ============================================================

import time
import subprocess
import csv
import os
import numpy as np
import threading
import queue
import re

import ttkbootstrap as tb
from tkinter import filedialog, messagebox

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from sklearn.linear_model import LinearRegression

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
devices = ["8.8.8.8", "1.1.1.1", "google.com"]
CSV_FILE = "C:/temp/rtt_log.csv"

os.makedirs("C:/temp", exist_ok=True)

rtt_values = []
time_values = []
states = []
t = 0

# Queue to handle threading and prevent UI freezing
ping_queue = queue.Queue()
is_pinging = False

# ------------------------------------------------------------
# RTT FUNCTION (THREADED & ACCURATE)
# ------------------------------------------------------------
def get_rtt_worker(host):
    """Runs in the background to prevent UI from freezing."""
    global is_pinging
    try:
        # CREATE_NO_WINDOW prevents command prompt flashing on Windows
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", host],
            capture_output=True, 
            text=True,
            startupinfo=startupinfo
        )
        
        # Parse actual ping time from terminal output using regex
        match = re.search(r"time[=<](\d+)ms", result.stdout)
        if match:
            rtt = float(match.group(1))
        else:
            rtt = None
    except Exception:
        rtt = None

    ping_queue.put(rtt)
    is_pinging = False

# ------------------------------------------------------------
# CLASSIFICATION
# ------------------------------------------------------------
def classify(rtt):
    if rtt is None:
        return "Offline", "danger"
    elif rtt < 50:
        return "Active", "success"
    else:
        return "Idle", "warning"

# ------------------------------------------------------------
# PDF REPORT
# ------------------------------------------------------------
def generate_pdf():
    if not rtt_values:
        messagebox.showwarning("Warning", "No data to generate a report.")
        return

    # Ask user where to save the file
    filepath = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        initialfile="RTT_Report.pdf",
        title="Save PDF Report",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not filepath:
        return # User cancelled

    try:
        doc = SimpleDocTemplate(filepath)
        styles = getSampleStyleSheet()
        content = []

        # Title
        content.append(Paragraph("RTT Device Tracking Report", styles["Title"]))
        content.append(Paragraph(f"Device: {device_var.get()}", styles["Normal"]))
        content.append(Paragraph(f"Total Readings: {len(rtt_values)}", styles["Normal"]))

        # Average
        valid_rtts = [r for r in rtt_values if r > 0]
        avg = sum(valid_rtts) / len(valid_rtts) if valid_rtts else 0
        content.append(Paragraph(f"Average RTT: {avg:.2f} ms", styles["Normal"]))

        # Stats
        active_count = states.count("Active")
        idle_count = states.count("Idle")
        offline_count = states.count("Offline")

        content.append(Paragraph(f"Active: {active_count}", styles["Normal"]))
        content.append(Paragraph(f"Idle: {idle_count}", styles["Normal"]))
        content.append(Paragraph(f"Offline: {offline_count}", styles["Normal"]))
        content.append(Paragraph(" ", styles["Normal"]))

        # Table
        table_data = [["Time (s)", "RTT (ms)", "State"]]
        for i in range(len(rtt_values)):
            table_data.append([
                str(time_values[i]),
                f"{rtt_values[i]:.2f}" if rtt_values[i] > 0 else "N/A",
                states[i]
            ])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))

        content.append(table)
        doc.build(content)
        messagebox.showinfo("Success", f"Report saved successfully to:\n{filepath}")

    except PermissionError:
        messagebox.showerror("Error", "Permission denied. Ensure the PDF is not open in another program.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")

# ------------------------------------------------------------
# AI PREDICTION
# ------------------------------------------------------------
def predict_rtt():
    valid_data = [(t_val, r_val) for t_val, r_val in zip(time_values, rtt_values) if r_val > 0]
    
    if len(valid_data) < 5:
        prediction_var.set("Need more successful pings")
        return

    # Extract valid times and rtts
    X = np.array([d[0] for d in valid_data]).reshape(-1, 1)
    y = np.array([d[1] for d in valid_data])

    model = LinearRegression()
    model.fit(X, y)

    pred = model.predict([[time_values[-1] + 1]])
    prediction_var.set(f"Predicted Next RTT: {abs(pred[0]):.2f} ms")

# ------------------------------------------------------------
# RESET DATA WHEN DEVICE CHANGES
# ------------------------------------------------------------
def on_device_change(*args):
    global t, rtt_values, time_values, states
    t = 0
    rtt_values.clear()
    time_values.clear()
    states.clear()
    
    rtt_var.set("--")
    status_var.set("--")
    status_label.configure(bootstyle="secondary")
    
    ax1.clear()
    ax2.clear()
    canvas.draw()

# ------------------------------------------------------------
# UPDATE LOOP (NON-BLOCKING)
# ------------------------------------------------------------
def update_loop():
    global t, is_pinging

    # Check if a ping result has returned
    if not ping_queue.empty():
        rtt = ping_queue.get()
        state, color = classify(rtt)
        value = 0 if rtt is None else rtt

        rtt_values.append(value)
        time_values.append(t)
        states.append(state)

        rtt_var.set(f"{value:.2f} ms" if rtt else "No Response")
        status_var.set(state)
        status_label.configure(bootstyle=color)

        try:
            with open(CSV_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([t, value, state])
        except:
            pass

        state_map = {"Offline": 0, "Active": 1, "Idle": 2}

        ax1.clear()
        ax1.plot(time_values, rtt_values, color="#17a2b8", marker="o", markersize=4)
        ax1.set_title("RTT (ms)")
        ax1.set_ylabel("Milliseconds")
        ax1.grid(True, linestyle="--", alpha=0.5)

        ax2.clear()
        ax2.plot(time_values, [state_map[s] for s in states], color="#ffc107", drawstyle="steps-post", marker="o", markersize=4)
        ax2.set_title("Device State")
        ax2.set_yticks([0, 1, 2])
        ax2.set_yticklabels(["Offline", "Active", "Idle"])
        ax2.grid(True, linestyle="--", alpha=0.5)

        fig.tight_layout()
        canvas.draw()
        t += 1

    # Start a new ping in the background if we aren't already waiting for one
    if not is_pinging:
        is_pinging = True
        threading.Thread(target=get_rtt_worker, args=(device_var.get(),), daemon=True).start()

    root.after(1000, update_loop)

# ------------------------------------------------------------
# UI SETUP
# ------------------------------------------------------------
root = tb.Window(themename="darkly")
root.title("RTT Tracker PRO")
root.geometry("700x800")

tb.Label(root, text="RTT Device Tracker", font=("Arial", 20, "bold")).pack(pady=10)

device_var = tb.StringVar(value=devices[0])
tb.OptionMenu(root, device_var, devices[0], *devices).pack(pady=5)

rtt_var = tb.StringVar(value="--")
tb.Label(root, text="Current RTT:", font=("Arial", 12)).pack()
tb.Label(root, textvariable=rtt_var, font=("Arial", 16, "bold"), foreground="#17a2b8").pack()

status_var = tb.StringVar(value="--")
tb.Label(root, text="Device State:", font=("Arial", 12)).pack()

status_label = tb.Label(root, textvariable=status_var, font=("Arial", 16, "bold"))
status_label.pack(pady=5)

prediction_var = tb.StringVar(value="Prediction: --")
tb.Label(root, textvariable=prediction_var).pack(pady=5)

btn_frame = tb.Frame(root)
btn_frame.pack(pady=10)
tb.Button(btn_frame, text="Predict Next RTT", bootstyle="success", command=predict_rtt).pack(side="left", padx=5)
tb.Button(btn_frame, text="Export PDF Report", bootstyle="info", command=generate_pdf).pack(side="left", padx=5)

# Graph Setup
fig = plt.Figure(figsize=(6, 5))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
fig.tight_layout()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)

# Attach the trace AFTER the graphs are created to prevent startup crashes
device_var.trace_add("write", on_device_change)

# Start Loop
update_loop()

root.mainloop()