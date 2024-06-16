let map;
let service;
let directionsService;
let directionsRenderer;

function initMapWithLocation(lat, lng) {
    const userLocation = { lat: lat, lng: lng };

    map = new google.maps.Map(document.getElementById('map'), {
        center: userLocation,
        zoom: 13
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    const request = {
        location: userLocation,
        radius: '5000',
        type: ['store'],
        keyword: 'vape'
    };

    service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, handleNearbyShops);
}

function handleNearbyShops(results, status) {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
        // Sort results by distance from the user's location
        results.sort((a, b) => {
            let distA = google.maps.geometry.spherical.computeDistanceBetween(
                new google.maps.LatLng(a.geometry.location.lat(), a.geometry.location.lng()),
                map.getCenter());
            let distB = google.maps.geometry.spherical.computeDistanceBetween(
                new google.maps.LatLng(b.geometry.location.lat(), b.geometry.location.lng()),
                map.getCenter());
            return distA - distB;
        });

        // Assuming the nearest shop is the first after sorting
        createMarker(results[0]);
        findRoute(results[0]);
    }
}


function createMarker(place) {
    new google.maps.Marker({
        map: map,
        position: place.geometry.location
    });
}

function findRoute(destination) {
    const request = {
        origin: map.getCenter(),
        destination: destination.geometry.location,
        travelMode: 'WALKING'
    };

    directionsService.route(request, function(result, status) {
        if (status === 'OK') {
            directionsRenderer.setDirections(result);
        }
    });
}
