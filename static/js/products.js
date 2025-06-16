document.addEventListener('DOMContentLoaded', function () {
    const items = document.querySelectorAll('.product-item');
    const mapContainer = document.getElementById('mapContainer');

    let map = L.map('map').setView([0, 0], 13);
    let marker;

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(map);

    items.forEach(item => {
        item.addEventListener('click', () => {
            const lat = item.getAttribute('data-lat');
            const lng = item.getAttribute('data-lng');

            if (lat && lng) {
                map.setView([lat, lng], 13);
                if (marker) {
                    marker.setLatLng([lat, lng]);
                } else {
                    marker = L.marker([lat, lng]).addTo(map);
                }
                mapContainer.style.display = 'block';
            } else {
                alert("Location not available for this product.");
            }
        });
    });
});