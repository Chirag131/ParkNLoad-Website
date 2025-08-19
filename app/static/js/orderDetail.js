

// Map functionality
function openFullMap() {
    // Center the full map view on the route in a new tab (fallback to Google Maps area)
    window.open('https://www.google.com/maps/@28.48,77.02,12z', '_blank');
}

(function() {
    const mapEl = document.getElementById('orderMap');
    if (!mapEl) return;
    const pickupAddress = mapEl.getAttribute('data-pickup') || '';
    const deliveryAddress = mapEl.getAttribute('data-delivery') || '';

    let mapInstance = null;
    let routeLayer = null;
    let pickupMarker = null;
    let deliveryMarker = null;

    async function geocode(address) {
        const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`;
        const res = await fetch(url, { headers: { 'Accept-Language': 'en' } });
        const data = await res.json();
        if (!data || data.length === 0) throw new Error('Address not found');
        return { lat: parseFloat(data[0].lat), lng: parseFloat(data[0].lon) };
    }

    async function fetchRoute(from, to) {
        const url = `https://router.project-osrm.org/route/v1/driving/${from.lng},${from.lat};${to.lng},${to.lat}?overview=full&geometries=geojson`;
        const res = await fetch(url);
        const data = await res.json();
        if (!data || !data.routes || data.routes.length === 0) throw new Error('Route not found');
        return data.routes[0].geometry; // GeoJSON LineString
    }

    function addMarkers(from, to) {
        if (pickupMarker) mapInstance.removeLayer(pickupMarker);
        if (deliveryMarker) mapInstance.removeLayer(deliveryMarker);

        pickupMarker = L.circleMarker([from.lat, from.lng], {
            color: '#16a34a', fillColor: '#16a34a', fillOpacity: 0.9, radius: 7, weight: 2
        }).addTo(mapInstance).bindPopup('<strong>Pickup</strong>');

        deliveryMarker = L.circleMarker([to.lat, to.lng], {
            color: '#f59e0b', fillColor: '#f59e0b', fillOpacity: 0.9, radius: 7, weight: 2
        }).addTo(mapInstance).bindPopup('<strong>Delivery</strong>');
    }

    function drawRoute(geojsonLine) {
        if (routeLayer) mapInstance.removeLayer(routeLayer);
        routeLayer = L.geoJSON(geojsonLine, {
            style: { color: '#2563eb', weight: 5, opacity: 0.9 }
        }).addTo(mapInstance);
        mapInstance.fitBounds(routeLayer.getBounds(), { padding: [30, 30] });
    }

    async function initMap() {
        if (!mapInstance) {
            mapInstance = L.map('orderMap').setView([28.48, 77.02], 12);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap contributors' }).addTo(mapInstance);
        }

        try {
            const [from, to] = await Promise.all([
                geocode(pickupAddress),
                geocode(deliveryAddress)
            ]);
            addMarkers(from, to);
            const route = await fetchRoute(from, to);
            drawRoute(route);
        } catch (e) {
            console.error('Map error:', e);
        }
    }

    window.orderMapController = {
        refresh: initMap
    };

    document.addEventListener('DOMContentLoaded', initMap);
})();

function refreshMap() {
    if (window.orderMapController) {
        window.orderMapController.refresh();
    }
}
