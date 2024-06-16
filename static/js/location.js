function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showMap, showError, {
            enableHighAccuracy: true,  // Use GPS and network signals for better accuracy
            timeout: 5000,             // Maximum time allowed to try obtaining a location
            maximumAge: 0              // Force the request to get fresh location data
        });
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
}

function showMap(position) {
    initMapWithLocation(position.coords.latitude, position.coords.longitude);
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            console.error("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            console.error("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            console.error("The request to get user location timed out.");
            break;
        default:
            console.error("An unknown error occurred.");
            break;
    }
}
