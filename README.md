# OmniWatch: Real-Time Process Monitoring Dashboard 🚀

A lightweight, dependency-free (frontend), real-time system monitoring utility designed to evaluate CPU, memory, Disk, and Running Processes directly from your browser. 

---

## 🏆 SIH Impact Statement

> *"A minimal, scalable alternative to heavy built-in or enterprise monitoring tools."*

This solution provides a **lightweight, real-time monitoring tool** that can be deployed in educational institutions, small businesses, low-resource systems, and edge devices. It ensures **efficient system management, early detection of performance issues, and improved operational reliability** without requiring expensive monitoring software or heavy agent installations. 

**Key Innovation**:
- **Zero Browser Dependencies**: Doesn't require React, Angular, or external UI libraries. Pure Vanilla JS/HTML/CSS.
- **Micro-Backend**: Uses a simple Flask wrapper around `psutil` operating at a ~20MB RAM footprint.
- **Cross-Platform Potential**: Readily works on Windows, Linux, and macOS without codebase modifications.

---

## ✨ Features

### 🖥 System Resource Monitoring
- **Real-Time Data**: Tracks CPU, Memory, and Disk usage via live polling (2s intervals).
- **Trend Visualization**: Dynamic HTML5 Canvas rendering of CPU and Memory behavior over the last 60 seconds (no external chart libraries used).

### ⚙️ Process Management
- **Live Process Table**: View PID, Name, CPU %, and Memory % updated dynamically.
- **Task Management**: Instantly sort and search running tasks. 
- **Secure Process Killing**: Terminate unneeded or rogue processes immediately from the dashboard (secured against killing core OS PIDs and the dashboard itself).

### 🧠 Intelligent System & UI
- **Smart AI Insights**: Detects anomalous behavior (e.g., detecting if a single app is consuming abnormal percentages of CPU).
- **Rich User Experience**: Smooth Neumorphic styling, Toast Alerts, and Native Dark/Light mode tracking.

---

## 🚀 Setup Instructions

Ensure you have **Python 3.x** installed. The project relies on minimal libraries: standard Flask routing and `psutil`.

### Quick Start (Windows)
1. Double-click the `start.bat` file in the root directory.
2. The script will automatically:
   - Install dependencies (`psutil`, `Flask`).
   - Run the Flask Backend minimised.
   - Boot up your default web browser to `http://127.0.0.1:5000`.

### Manual Start (Cross-Platform)

**1. Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**2. Start the Backend**
```bash
python app.py
```

**3. Open Browser**
Navigate to `http://127.0.0.1:5000` to view OmniWatch.

---

## 🏗️ Project Architecture Framework

```
process-dashboard/
│
├── backend/                  # Python lightweight API Layer
│   ├── app.py                # Flask routing and frontend server
│   ├── system_monitor.py     # psutil abstraction for OS metrics
│   ├── process_handler.py    # psutil process enumeration and SIGTERM handlers
│   └── requirements.txt      
│
├── frontend/                 # Vanilla Web implementation
│   ├── index.html            # Semantic web struct
│   ├── style.css             # Fluid, responsive theming and CSS vars
│   └── script.js             # Async Fetch routines, Canvas drawings
│
├── start.bat                 # 1-Click Bootstrap Script
└── README.md                 # Project Overview
```
