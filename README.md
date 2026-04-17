# RTT-device-tracker
This project tracks device activity using Round Trip Time (RTT). It classifies devices as Active, Idle, or Offline.
# 🚀 Device Activity Tracking Using RTT-Based Analysis

A lightweight, privacy-friendly system to monitor device activity using **Round Trip Time (RTT)**.  
The project classifies devices as **Active, Idle, or Offline** based on network response time without accessing any internal or sensitive data.

---

## 📌 Overview

Traditional device monitoring systems rely on intrusive methods like authentication logs or packet inspection.  
This project introduces a **non-intrusive approach** using RTT (network latency) to determine device activity.

✔ No data access required  
✔ Real-time monitoring  
✔ Simple and efficient  
✔ Privacy-aware  

---

## 🎯 Features

- 📡 Real-time RTT measurement using ping
- 🟢 Device state classification (Active / Idle / Offline)
- 📊 Live graph visualization (RTT vs Time)
- 🤖 AI-based RTT prediction (Linear Regression)
- 📄 Automated PDF report generation
- 🌐 Multi-device tracking support

---

## 🧠 How It Works

1. User selects a target device (IP or domain)
2. System sends a ping request
3. RTT (response time) is calculated
4. RTT is compared with thresholds:
   - RTT < 50 ms → **Active**
   - RTT < 150 ms → **Idle**
   - No response → **Offline**
5. Results are displayed in GUI
6. Data is stored for graphs and prediction

---

## 🏗️ System Architecture

User Interface → RTT Measurement → Data Processing → Classification → Output Display

---

## 🧩 Modules

- RTT Measurement Module
- Data Processing Module
- Classification Module
- Visualization Module
- Prediction Module
- Report Generation Module

---

## 🛠️ Technologies Used

- Python
- Matplotlib (Visualization)
- NumPy (Numerical Processing)
- Scikit-learn (Machine Learning)
- ReportLab (PDF Generation)
- Tkinter (GUI)

---

## 📦 Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/your-username/rtt-device-tracker.git
cd rtt-device-tracker
