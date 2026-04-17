# 🚀 Device Activity Tracking Using RTT-Based Analysis

## 📌 Overview

This project implements a **non-intrusive device monitoring system** using **Round Trip Time (RTT)** analysis.
It determines whether a device is **Active, Idle, or Offline** by measuring network response time — without accessing any private data.

The system provides **real-time monitoring, visualization, prediction, and reporting**, making it suitable for academic and practical network analysis.

---

## 🎯 Key Features

* 📡 Real-time RTT monitoring
* 📊 Live graph visualization
* 🔄 Device state classification (Active / Idle / Offline)
* 🤖 AI-based RTT prediction
* 📄 Automatic PDF report generation
* 🌐 Multi-device support
* 🔒 Privacy-friendly (non-intrusive)

---

## 🧠 Concept

The system is based on the concept of **Round Trip Time (RTT)**, which measures the time taken for a signal to travel from the source to a device and back.

Based on RTT values:

* **< 50 ms** → Active
* **50–150 ms** → Idle
* **No response** → Offline

---

## 🛠️ Technologies Used

* **Python** – Core programming
* **Matplotlib** – Graph visualization
* **NumPy** – Numerical operations
* **Scikit-learn** – Machine learning (Linear Regression)
* **ReportLab** – PDF generation
* **Tkinter** – GUI interface

---

## 📂 Project Structure

```
RTT-Device-Tracker/
│
├── code/
│   └── main.py
│
├── screenshots/
│   ├── gui.png
│   ├── graph.png
│
├── report/
│   └── report.pdf
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ▶️ How to Run

### 1️⃣ Clone Repository

```
git clone https://github.com/syedfurqhaanali/RTT-Device-Tracker.git
cd RTT-Device-Tracker
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Run Application

```
python main.py
```

---

## 📸 Output Screens

### 🔹 GUI Dashboard

<img width="1600" height="851" alt="GUI dashboard" src="https://github.com/user-attachments/assets/3dec1de9-5241-43cc-a60b-ad19894eea00" />



### 🔹 Real-Time Graph

<img width="1600" height="854" alt="real time graph" src="https://github.com/user-attachments/assets/5d978ea9-5b47-41a5-8519-bc74fc9e191d" />


### 🔹 PDF Report

<img width="534" height="743" alt="PDF report" src="https://github.com/user-attachments/assets/3f364821-a0db-4854-9bdb-2b663cc7e168" />


---

## 📊 System Workflow

1. User selects device
2. System sends ping request
3. RTT is calculated
4. Device state is classified
5. Results displayed in GUI
6. Graph updates in real-time
7. Optional: Prediction & PDF generation

---

## ✅ Advantages

* Simple and lightweight
* No access to private data
* Real-time monitoring
* Easy to implement
* Scalable for future use

---

## ⚠️ Limitations

* Depends on network conditions
* Not 100% accurate in high-latency environments
* Basic classification thresholds

---

## 🔮 Future Enhancements

* Advanced AI models for anomaly detection
* Web / mobile application version
* Cloud-based monitoring
* Large-scale network support
* Enhanced visualization dashboard

---

## 📚 Use Cases

* Network monitoring
* Cybersecurity training
* IoT device tracking
* Educational projects

---

## 👨‍💻 Author

**Syed Furqhaan Ali**
B.Tech / Diploma Student
Department of Computer Science

---

## 📌 License

This project is for **educational purposes**.

---

## ⭐ Support

If you like this project:

* ⭐ Star the repository
* 🍴 Fork it
* 📢 Share with others

---

## 💬 Final Note

This project demonstrates how **network timing behavior can be used for device activity tracking without compromising privacy**.
