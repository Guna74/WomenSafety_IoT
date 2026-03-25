import asyncio
import time
import random
import requests
import os

PORT = os.getenv("PORT", "8000")
LOCAL_SENSOR_URL = f"http://127.0.0.1:{PORT}/sensor"

class SimulatorConfig:
    enabled = True
    state = "SAFE"
    frequency_ms = 2000
    
    # Internal vitals start points
    hr = 75.0
    temp = 36.8
    motion = 0.5
    lat = 17.3850
    lon = 78.4867
    
    state_override_end_time = 0

async def run_simulator():
    """Background task that loops forever while enabled."""
    print("Background Simulator running with smooth mean-reversion...")
    while True:
        if not SimulatorConfig.enabled:
            await asyncio.sleep(1)
            continue
            
        now = time.time()
        
        # Auto-revert logic
        if SimulatorConfig.state != "SAFE" and now > SimulatorConfig.state_override_end_time:
            SimulatorConfig.state = "SAFE"
            print("Simulator auto-reverted to SAFE")

        # Smooth Random Walk with Mean Reversion
        if SimulatorConfig.state == "SAFE":
            target_hr = 75.0
            target_temp = 36.8
            target_motion = 0.5
            
            # Move 10% towards target, plus a small random jitter
            SimulatorConfig.hr += (target_hr - SimulatorConfig.hr) * 0.1 + random.uniform(-1.0, 1.0)
            SimulatorConfig.temp += (target_temp - SimulatorConfig.temp) * 0.1 + random.uniform(-0.02, 0.02)
            SimulatorConfig.motion += (target_motion - SimulatorConfig.motion) * 0.2 + random.uniform(-0.2, 0.2)
            
            # Hard bounds
            SimulatorConfig.hr = max(60, min(SimulatorConfig.hr, 90))
            SimulatorConfig.motion = max(0, SimulatorConfig.motion)
            voice = ""
            
        elif SimulatorConfig.state == "EXERCISE":
            target_hr = 145.0
            target_temp = 37.6
            target_motion = 8.0
            
            SimulatorConfig.hr += (target_hr - SimulatorConfig.hr) * 0.2 + random.uniform(-2.0, 2.0)
            SimulatorConfig.temp += (target_temp - SimulatorConfig.temp) * 0.1 + random.uniform(-0.05, 0.05)
            SimulatorConfig.motion += (target_motion - SimulatorConfig.motion) * 0.2 + random.uniform(-1.0, 1.0)
            voice = ""
            
        elif SimulatorConfig.state == "PANIC":
            target_hr = 165.0
            target_motion = 15.0
            
            SimulatorConfig.hr += (target_hr - SimulatorConfig.hr) * 0.3 + random.uniform(-3.0, 3.0)
            SimulatorConfig.temp += random.uniform(-0.1, 0.1)
            SimulatorConfig.motion += (target_motion - SimulatorConfig.motion) * 0.3 + random.uniform(-2.0, 2.0)
            
            # Panic voice 30% of the time during panic state
            voice = random.choice(["", "help", "", "aaaah"]) if random.random() > 0.7 else ""

        payload = {
            "heart_rate": round(SimulatorConfig.hr, 2),
            "temperature": round(SimulatorConfig.temp, 2),
            "motion": round(SimulatorConfig.motion, 2),
            "voice": voice,
            "lat": SimulatorConfig.lat,
            "lon": SimulatorConfig.lon
        }

        try:
            requests.post(LOCAL_SENSOR_URL, json=payload, timeout=2)
        except Exception:
            pass

        await asyncio.sleep(SimulatorConfig.frequency_ms / 1000.0)
