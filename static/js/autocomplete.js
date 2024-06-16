
function initAutocomplete() {
    var searchInput = document.getElementById('search-input');

    var autocomplete = new google.maps.places.Autocomplete(searchInput, {
        types: ['geocode'], // Specify the type of places to search
    });

    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            console.log("Returned place contains no geometry");
            return;
        }
        // You can do something with the selected place here, like showing it on the map or getting more details
    });
}

// Ensure this function is called when the page is loaded
document.addEventListener("DOMContentLoaded", function() {
    initAutocomplete();
});