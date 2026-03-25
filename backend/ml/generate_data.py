import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=5000):
    np.random.seed(42)
    data = []

    for _ in range(num_samples):
        state = np.random.choice(['SAFE', 'EXERCISE', 'PANIC'], p=[0.6, 0.2, 0.2])

        if state == 'SAFE':
            # Resting or normal walking
            hr = np.random.normal(80, 15)  # 60 - 110 approx
            temp = np.random.normal(36.8, 0.3)
            motion = np.random.normal(2, 1) # Low motion
            voice_panic_score = 0  # No panic voice
            
        elif state == 'EXERCISE':
            # Running, cardio, rigid activity
            hr = np.random.normal(150, 20) # 130 - 190 approx
            temp = np.random.normal(37.5, 0.4) # Slightly elevated temp
            motion = np.random.normal(8, 2) # High consistent motion
            voice_panic_score = 0
            
        elif state == 'PANIC':
            # Assault or extreme panic attack
            # Characterized by either erratic high motion OR low motion with very high HR
            # AND often a panic voice
            is_assault = np.random.rand() > 0.5
            
            if is_assault:
                hr = np.random.normal(160, 20)
                temp = np.random.normal(37.1, 0.5)
                motion = np.random.normal(12, 3) # Erratic, very high motion
            else:
                # Panic attack (freezing)
                hr = np.random.normal(140, 15)
                temp = np.random.normal(36.5, 0.5) # Cold sweat
                motion = np.random.normal(1, 0.5) # Low motion
                
            # Usually panic word is spoken during panic/assault, but not 100% of the time. Let's make it 80% likely.
            voice_panic_score = 1 if np.random.rand() < 0.8 else 0

        # Clipping values to be realistic
        hr = np.clip(hr, 50, 210)
        temp = np.clip(temp, 35.0, 40.0)
        motion = np.clip(motion, 0, 20)

        data.append([hr, temp, motion, voice_panic_score, state])

    df = pd.DataFrame(data, columns=['heart_rate', 'temperature', 'motion', 'voice_panic_score', 'label'])
    
    # Save to data directory
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/dummy_data.csv', index=False)
    print(f"Successfully generated {num_samples} samples of synthetic data at data/dummy_data.csv")

if __name__ == "__main__":
    generate_synthetic_data()
