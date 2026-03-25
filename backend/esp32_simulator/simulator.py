import requests
import time
import random

URL = "http://127.0.0.1:8000/sensor"

class HumanSimulator:
    def __init__(self):
        self.state = "SAFE"
        self.hr = 75.0
        self.temp = 36.8
        self.motion = 2.0
        self.lat = 17.3850
        self.lon = 78.4867
        
    def transition(self):
        # Apply random walks with boundaries
        if self.state == "SAFE":
            self.hr += random.uniform(-2, 2)
            self.hr = max(60, min(self.hr, 100))
            self.temp += random.uniform(-0.1, 0.1)
            self.temp = max(36.5, min(self.temp, 37.2))
            self.motion = random.uniform(0, 3)
            voice = ""
            
        elif self.state == "EXERCISE":
            self.hr += random.uniform(-5, 5)
            self.hr = max(130, min(self.hr, 180))
            self.temp += random.uniform(-0.1, 0.1)
            self.temp = max(37.0, min(self.temp, 38.0))
            self.motion = random.uniform(5, 12)
            voice = ""
            
        elif self.state == "PANIC":
            self.hr += random.uniform(-5, 5)
            self.hr = max(140, min(self.hr, 190))
            self.motion = random.uniform(10, 20) # Erratic motion
            self.temp += random.uniform(-0.2, 0.2)
            voice = random.choice(["", "help", "", "aaaah"])
            
        return {
            "heart_rate": round(self.hr, 2),
            "temperature": round(self.temp, 2),
            "motion": round(self.motion, 2),
            "voice": voice,
            "lat": self.lat,
            "lon": self.lon
        }

def run_simulator():
    sim = HumanSimulator()
    print("Realistic IoT Simulator Started.")
    print("Press Ctrl+C to stop.")
    
    cycle = 0
    try:
        while True:
            # Switch states naturally every few seconds for the demo
            if cycle == 0:
                print("\n>>> SIMULATING: Resting (SAFE)")
                sim.state = "SAFE"
            elif cycle == 10:
                print("\n>>> SIMULATING: Jogging (EXERCISE)")
                sim.state = "EXERCISE"
                sim.hr = 130  # sudden jump to jogging HR
            elif cycle == 20:
                print("\n>>> SIMULATING: Assault / Panic Attack (PANIC)")
                sim.state = "PANIC"
                sim.hr = 150 # sharp jump
                
            if cycle >= 28:
                cycle = -1 # Loop back
                
            payload = sim.transition()
            
            try:
                r = requests.post(URL, json=payload)
                resp = r.json()
                print(f"[{sim.state}] -> HR: {payload['heart_rate']} | Motion: {payload['motion']} | Voice: '{payload['voice']}' -> Backend Risk: {resp['risk_level']}")
            except requests.exceptions.ConnectionError:
                print("Backend not reachable. Start `uvicorn main:app` first.")
                
            time.sleep(2)
            cycle += 1
            
    except KeyboardInterrupt:
        print("\nSimulator stopped.")

if __name__ == "__main__":
    run_simulator()
