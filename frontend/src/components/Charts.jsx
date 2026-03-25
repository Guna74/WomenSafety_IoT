import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend 
} from 'recharts';
import { fetchHistory, fetchAggregatedHistory } from '../services/api';

const Charts = () => {
  const [activeTab, setActiveTab] = useState('live'); // 'live' or 'historical'
  
  // Live State
  const [dataLimit, setDataLimit] = useState(50);
  const [liveData, setLiveData] = useState([]);
  
  // Historical State
  const [period, setPeriod] = useState('hours'); // 'hours', 'days', 'weeks'
  const [aggData, setAggData] = useState([]);

  useEffect(() => {
    let interval;
    const fetchCharts = async () => {
      if (activeTab === 'live') {
        const history = await fetchHistory(dataLimit);
        // Reverse so oldest is left, newest is right
        setLiveData(history.reverse().map((d, i) => ({
          time: new Date(d.timestamp).toLocaleTimeString(),
          heartRate: d.heart_rate,
          motion: d.motion,
        })));
      } else {
        const agg = await fetchAggregatedHistory(period);
        setAggData(agg.map(d => ({
          time: d.time,
          avgHeartRate: d.heart_rate,
          avgMotion: d.motion
        })));
      }
    };

    fetchCharts();
    interval = setInterval(fetchCharts, 2000); // refresh every 2s

    return () => clearInterval(interval);
  }, [activeTab, dataLimit, period]);

  return (
    <div className="card charts-card">
      <div className="card-header chart-tabs">
        <div className="tab-group">
          <button className={`tab-btn ${activeTab === 'live' ? 'active' : ''}`} onClick={() => setActiveTab('live')}>
            Live Vitals
          </button>
          <button className={`tab-btn ${activeTab === 'historical' ? 'active' : ''}`} onClick={() => setActiveTab('historical')}>
            Historical Averages
          </button>
        </div>
        
        {activeTab === 'live' && (
          <div className="slider-group row-slider">
            <label>Zoom (Data Points): {dataLimit}</label>
            <input type="range" min="10" max="250" step="10" value={dataLimit} onChange={(e) => setDataLimit(Number(e.target.value))} />
          </div>
        )}

        {activeTab === 'historical' && (
          <div className="dropdown-group">
            <label>Group By:</label>
            <select value={period} onChange={(e) => setPeriod(e.target.value)} className="chart-select">
              <option value="hours">Past Hours</option>
              <option value="days">Past Days</option>
              <option value="weeks">Past Weeks</option>
            </select>
          </div>
        )}
      </div>

      <div className="chart-container" style={{ height: '350px', marginTop: '20px' }}>
        <ResponsiveContainer width="100%" height="100%">
          {activeTab === 'live' ? (
            <LineChart data={liveData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="time" stroke="#666" fontSize={10} minTickGap={30} />
              <YAxis yAxisId="left" domain={['auto', 'auto']} stroke="var(--accent-red)" />
              <YAxis yAxisId="right" orientation="right" domain={[0, 25]} stroke="var(--accent-blue)" />
              <Tooltip contentStyle={{ backgroundColor: '#111', borderColor: '#333' }} />
              <Legend />
              <Line yAxisId="left" name="Heart Rate (bpm)" type="monotone" dataKey="heartRate" stroke="var(--accent-red)" strokeWidth={2} dot={false} isAnimationActive={false} />
              <Line yAxisId="right" name="Motion (g)" type="monotone" dataKey="motion" stroke="var(--accent-blue)" strokeWidth={2} dot={false} isAnimationActive={false} />
            </LineChart>
          ) : (
            <BarChart data={aggData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="time" stroke="#666" fontSize={10} />
              <YAxis yAxisId="left" domain={[60, 'auto']} stroke="var(--accent-red)" />
              <YAxis yAxisId="right" orientation="right" domain={[0, 20]} stroke="var(--accent-blue)" />
              <Tooltip contentStyle={{ backgroundColor: '#111', borderColor: '#333' }} cursor={{fill: 'transparent'}} />
              <Legend />
              <Bar yAxisId="left" name="Avg HR" dataKey="avgHeartRate" fill="var(--accent-red)" radius={[4, 4, 0, 0]} />
              <Bar yAxisId="right" name="Avg Motion" dataKey="avgMotion" fill="var(--accent-blue)" radius={[4, 4, 0, 0]} />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Charts;
