# WomenSafety IoT 🛡️ 

A powerful **Full-Stack IoT Safety System** utilizing Machine Learning, Real-Time Cloud Telemetry, and a Dynamic React Dashboard.

The system is designed to seamlessly process continuous physiological sensor data (Heart Rate, Body Temperature, Motion Intensity) and instantly classify the user's current physical state as **SAFE**, **EXERCISE**, or **PANIC (EMERGENCY)** using advanced AI.

---

## 🌟 Key Features

* **Intelligent AI Validation**: Utilizes a pre-trained **RandomForestClassifier** (98% accuracy) strictly tracking physiological states to eliminate false positives. The backend enforces a >2 Second Confirmation Rule before validating a biological emergency.
* **Live React Dashboard**: A completely dynamic Control Panel showcasing a beautiful Digital Twin, live mapping via Leaflet, and adjustable React Recharts.
* **Native Simulation**: Features a built-in asynchronous Python background simulator configured with a Mean-Reverting statistical algorithm. It accurately generates human-like continuous vital fluctuations instantly without requiring physical IoT micro-controllers attached!
* **Cloud & Edge Foundation**: Engineered for cloud hosting effortlessly tracking Historical aggregations of the previous days and weeks via centralized SQLite tracking, demonstrating true IoT streaming capabilities.

---

## 🛠️ Technology Stack

* **Backend Environment**: Python 3.10+, FastAPI, Uvicorn, SQLite3.
* **Machine Learning Ops**: Scikit-Learn 1.6.1, Pandas 2.2.3, Joblib 1.4.2.
* **Frontend Visualization**: React (Vite), React-Leaflet, Recharts, Lucide-React.

---

## 🚀 Local Setup & Installation

Follow these steps to spin up the entire architecture on your own laptop!

### 1. The Machine Learning Backend
Open your terminal and navigate to the `backend` folder. It is highly recommended to use a Virtual Environment so you do not accidentally overwrite your computer's global packages!

```bash
cd backend
python -m venv venv

# Activate the environment:
# On Windows:
.\venv\Scripts\Activate.ps1
# On MacOS/Linux:
source venv/bin/activate

# Install the strict dependencies:
pip install -r requirements.txt
```

Start the cloud API and background Human Simulator:
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Your backend is now running at `http://localhost:8000`.

### 2. The React Frontend
Open a **second** terminal window and navigate to the `frontend` folder.

```bash
cd frontend
npm install

# Start the Vite dashboard:
npm run dev
```
Open `http://localhost:3000` in your web browser. You will instantly see the dynamic digital twin connected to the live backend stream!

---

## 🌍 Cloud Deployment Strategy

The architecture is explicitly programmed to be pushed to the public Internet continuously!

* **Deploying the Backend (Render)**
  The repository is structured with a root `.python-version` file to lock remote hosting capabilities instantly. You can load this exact Github URL into [Render.com](https://render.com) using a generic **Web Service**. It will extract the `$PORT` automatically and spin up the backend safely.
* **Deploying the Frontend (Netlify or Vercel)**
  Load your GitHub Repository into [Netlify](https://netlify.com) or [Vercel](https://vercel.com).
  Simply set the **Publish Directory** to `frontend/dist` and create a single Environment Variable named `VITE_API_URL` containing your live Render backend URL!

*(The `_redirects` SPA configuration file is already bundled for flawless Netlify deployments).*

---
> **Developer Note on Edge Computing:** 
> While this repository simulates cloud streams entirely via `background_simulator.py`, building the absolute physical micro-controller counterpart (e.g., ESP32 C++) enables Edge Computing capabilities. Programming the ESP32 to only communicate with the cloud REST API when recognizing irregular heart rate thresholds locally drastically preserves cloud bandwidth and battery consumption.
