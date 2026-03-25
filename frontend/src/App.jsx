import React, { useState, useEffect } from 'react';
import { fetchDigitalTwin, fetchHistory, triggerSimulator, changeFrequency } from './services/api';
import DigitalTwin from './components/DigitalTwin';
import Charts from './components/Charts';
import MapView from './components/MapView';
import { ShieldAlert, RefreshCw, Settings, Play, Flame } from 'lucide-react';

function App() {
  const [twin, setTwin] = useState(null);
  const [history, setHistory] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  
  // Control Panel state
  const [freq, setFreq] = useState(2000);

  useEffect(() => {
    const pollData = async () => {
      const liveData = await fetchDigitalTwin();
      if (liveData) {
        setTwin(liveData);
        setLastUpdated(new Date());
      }
    };

    pollData();
    // Default dashboard polling is tight to reflect whatever the server has instantly
    const interval = setInterval(pollData, 1000); 
    return () => clearInterval(interval);
  }, []);

  const handleFreqChange = (e) => {
    const ms = parseInt(e.target.value, 10);
    setFreq(ms);
    changeFrequency(ms);
  };

  // We rely strictly on the sustained 2s rule flag passed from backend
  const isPanic = twin?.alert_active; 
  const imminentRisk = twin?.risk === 'PANIC'; // The model says panic, but >2s verification might be pending

  return (
    <div className={`dashboard-container ${isPanic ? 'panic-mode' : (imminentRisk ? 'warning-mode' : '')}`}>
      <header className="dashboard-header">
        <div className="logo">
          <ShieldAlert size={36} color={isPanic ? 'var(--accent-red)' : (imminentRisk ? 'var(--accent-yellow)' : 'var(--accent-blue)')} />
          <h1>Women Safety System</h1>
        </div>
        
        <div className="control-panel">
           <div className="slider-group">
              <label>Data Freq: {freq}ms</label>
              <input type="range" min="500" max="10000" step="500" value={freq} onChange={handleFreqChange} />
           </div>
           
           <button onClick={() => triggerSimulator('EXERCISE', 15)} className="btn btn-blue">
             <Play size={16}/> Force Exercise
           </button>
           <button onClick={() => triggerSimulator('PANIC', 10)} className="btn btn-red">
             <Flame size={16}/> Force PANIC (10s)
           </button>
        </div>

        <div className="status-indicator">
          <span className="last-updated">
            <RefreshCw size={14} className="spin-icon" /> 
            Updated: {lastUpdated.toLocaleTimeString()}
          </span>
        </div>
      </header>

      <main className="dashboard-grid">
        <div className="grid-left">
          <DigitalTwin data={twin} />
          <MapView data={twin} />
        </div>
        <div className="grid-right">
          <Charts history={history} />
        </div>
      </main>
    </div>
  );
}

export default App;
