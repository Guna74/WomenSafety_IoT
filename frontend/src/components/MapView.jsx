import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import { Navigation } from 'lucide-react';

// Fix Leaflet's default icon issue statically
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Create a custom red icon for panic mode
const redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Component to dynamically recenter the map when coordinates change
const MapUpdater = ({ center }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center, map.getZoom(), { animate: true });
  }, [center, map]);
  return null;
};

const MapView = ({ data }) => {
  if (!data || !data.lat || !data.lon) return <div className="card loading">Waiting for GPS...</div>;

  const position = [data.lat, data.lon];
  const isPanic = data.risk === 'PANIC';

  return (
    <div className="card map-card">
      <div className="card-header">
        <h2>Live Location</h2>
        <Navigation size={24} color={isPanic ? 'var(--accent-red)' : 'var(--accent-blue)'} />
      </div>
      <div className="map-wrapper" style={{ height: '300px', width: '100%', marginTop: '15px', borderRadius: '12px', overflow: 'hidden', border: isPanic ? '2px solid var(--accent-red)' : '1px solid #333' }}>
        <MapContainer center={position} zoom={13} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MapUpdater center={position} />
          <Marker position={position} icon={isPanic ? redIcon : new L.Icon.Default()}>
            <Popup>
              <strong>{isPanic ? 'EMERGENCY LOCATION!' : 'Current Location'}</strong><br />
              Lat: {data.lat}<br />
              Lon: {data.lon}
            </Popup>
          </Marker>
        </MapContainer>
      </div>
    </div>
  );
};

export default MapView;
