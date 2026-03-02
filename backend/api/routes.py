from fastapi import APIRouter
from ml.predict import predict_risk
from utils.helpers import get_latest_state, save_to_db, get_history

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    return {
        "history": get_history()
    }

@router.post("/sensor")
def receive_sensor(data: dict):
    print("Incoming data:", data) # logs
    risk = predict_risk(data)

    print("Predicted risk:", risk)
    print("Location:", data.get("lat"), data.get("lon"))
    
    save_to_db(data, risk)   

    vibrate = True if risk == "EMERGENCY" else False
    message = "Emergency detected! Sending help signal" if risk == "EMERGENCY" else "No emergency. You are safe"
    return {
        "risk_level": risk,
        "alert": vibrate,
        "vibration": vibrate,
        "message": message
    }

@router.get("/digital_twin")
def digital_twin():
    return get_latest_state()
