const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const fetchDigitalTwin = async () => {
  try {
    const response = await fetch(`${API_URL}/digital_twin`);
    if (!response.ok) return null;
    return await response.json();
  } catch (error) {
    return null;
  }
};

export const fetchHistory = async (limit = 50) => {
  try {
    const response = await fetch(`${API_URL}/dashboard?limit=${limit}`);
    if (!response.ok) return [];
    const data = await response.json();
    return data.history || [];
  } catch (error) {
    return [];
  }
};

export const fetchAggregatedHistory = async (period = "hours") => {
  try {
    const response = await fetch(`${API_URL}/dashboard/aggregated?period=${period}`);
    if (!response.ok) return [];
    const data = await response.json();
    return data.history || [];
  } catch (error) {
    return [];
  }
};

export const triggerSimulator = async (stateStr, duration_sec = 15) => {
  try {
    await fetch(`${API_URL}/simulator/trigger`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state: stateStr, duration_sec })
    });
  } catch (error) {}
};

export const changeFrequency = async (frequency_ms) => {
  try {
    await fetch(`${API_URL}/simulator/config`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ frequency_ms })
    });
  } catch (error) {}
};
