import React from 'react';
import { Heart, Thermometer, Activity, ShieldAlert, ShieldCheck, Footprints } from 'lucide-react';

const DigitalTwin = ({ data }) => {
  if (!data) return <div className="card loading">Loading Twin...</div>;

  const isPanic = data.risk === 'PANIC';
  const isExercise = data.risk === 'EXERCISE';
  
  let riskColor = 'var(--accent-green)';
  let riskIcon = <ShieldCheck size={32} />;
  let riskText = 'SAFE';

  if (isExercise) {
    riskColor = 'var(--accent-yellow)';
    riskIcon = <Activity size={32} />;
    riskText = 'EXERCISE';
  } else if (isPanic) {
    riskColor = 'var(--accent-red)';
    riskIcon = <ShieldAlert size={32} />;
    riskText = 'EMERGENCY / PANIC';
  }

  return (
    <div className={`card digital-twin ${isPanic ? 'panic-pulse' : ''}`}>
      <div className="card-header">
        <h2>Live Digital Twin</h2>
        <div className="status-badge" style={{ backgroundColor: riskColor }}>
          {riskText}
        </div>
      </div>
      
      <div className="twin-metrics">
        <div className="metric">
          <Heart size={28} className="metric-icon" color="var(--accent-red)" style={{ animation: data.heart_rate > 100 ? 'pulse 0.5s infinite' : 'pulse 1s infinite' }} />
          <div>
            <span className="metric-val">{data.heart_rate}</span> bpm
            <p className="metric-label">Heart Rate</p>
          </div>
        </div>

        <div className="metric">
          <Thermometer size={28} className="metric-icon" color="var(--accent-yellow)" />
          <div>
            <span className="metric-val">{data.temperature}</span> °C
            <p className="metric-label">Body Temp</p>
          </div>
        </div>

        <div className="metric">
          <Footprints size={28} className="metric-icon" color="var(--accent-blue)" />
          <div>
            <span className="metric-val">{data.motion}</span> g
            <p className="metric-label">Motion Intensity</p>
          </div>
        </div>
      </div>
      
      {isPanic && (
        <div className="panic-alert-box">
          <ShieldAlert size={24} />
          <strong>EMERGENCY DETECTED! Sending Help!</strong>
        </div>
      )}
    </div>
  );
};

export default DigitalTwin;
