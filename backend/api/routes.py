from fastapi import APIRouter
from pydantic import BaseModel
import time

from ml.predict import predict_risk
from utils.helpers import get_latest_state, save_to_db, get_history, get_aggregated_history
from background_simulator import SimulatorConfig

router = APIRouter()

# Memory structure to track sustained panic
panic_history = []
last_alert_state = False

def is_panic_sustained(current_risk):
    global panic_history, last_alert_state
    now = time.time()
    
    if current_risk == 'PANIC':
        panic_history.append(now)
        # Keep only timestamps within the last 4 seconds
        panic_history = [t for t in panic_history if now - t <= 4]
        
        if len(panic_history) >= 2 and (now - panic_history[0]) >= 2.0:
            last_alert_state = True
            return True
        last_alert_state = False
        return False
    else:
        panic_history.clear()
        last_alert_state = False
        return False

@router.get("/dashboard")
def dashboard(limit: int = 50):
    return {
        "history": get_history(limit=limit)
    }
    
@router.get("/dashboard/aggregated")
def dashboard_aggregated(period: str = "hours"):
    return {
        "history": get_aggregated_history(period=period)
    }

@router.post("/sensor")
def receive_sensor(data: dict):
    risk = predict_risk(data)
    save_to_db(data, risk)   
    alert_active = is_panic_sustained(risk)
    message = "EMERGENCY: Sustained Attack Detected!" if alert_active else ("Verifying threat..." if risk == "PANIC" else "Safe")

    return {
        "risk_level": risk,
        "alert": alert_active,
        "vibration": alert_active,
        "message": message,
        "sustained_panic": alert_active
    }

@router.get("/digital_twin")
def digital_twin():
    state = get_latest_state()
    state["alert_active"] = last_alert_state
    return state

class TriggerRequest(BaseModel):
    state: str
    duration_sec: int = 15

@router.post("/simulator/trigger")
def trigger_simulator(req: TriggerRequest):
    SimulatorConfig.state = req.state
    SimulatorConfig.state_override_end_time = time.time() + req.duration_sec
    if req.state == "PANIC":
        SimulatorConfig.hr = 150
        SimulatorConfig.motion = 15
    elif req.state == "EXERCISE":
        SimulatorConfig.hr = 135
        SimulatorConfig.motion = 8
    return {"message": f"Simulator forced to {req.state} for {req.duration_sec}s"}

class ConfigRequest(BaseModel):
    frequency_ms: int

@router.post("/simulator/config")
def config_simulator(req: ConfigRequest):
    SimulatorConfig.frequency_ms = req.frequency_ms
    return {"message": f"Frequency updated to {req.frequency_ms}ms"}
