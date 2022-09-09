$.getScript("https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initMap)
})

function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    document.getElementById('map-route').style.height = '400px';
    var map = new google.maps.Map(document.getElementById('map-route'), {
        zoom: 1,
        center: {lat: lat_a, lng: long_a}
    });
    directionsDisplay.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsDisplay);
}

const waypts = [
        {location: {lat: lat_c, lng: long_c},
        stopover: false},
        {location: {lat: lat_d, lng: long_d},
        stopover: false},
        {location: {lat: lat_e, lng: long_e},
        stopover: false},
        {location: {lat: lat_f, lng: long_f},
        stopover: false}
        ];

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    directionsService.route({
        origin: origin,
        destination: destination,
        waypoints: waypts,
        optimizeWaypoints: true,
        travelMode: google.maps.TravelMode.DRIVING,
    }, function(response, status) {
      if (status === 'OK') {
        directionsDisplay.setDirections(response);
      } else {
        alert('Directions request failed due to ' + status);
      }
    });
}

function reload(){
setTimeout(()=>{
  $.ajax({
    data: {
        'placa': placa,
        "posicion":posicion,
        "csrfmiddlewaretoken": csrf_token,
    },
    url: url,
    type: method,
    success: function(data) {
      google_api_key = JSON.stringify(data['google_api_key'])
      lat_a = parseFloat(JSON.stringify(data['lat_a']));
      long_a = parseFloat(JSON.stringify(data['long_a']));
      lat_b = parseFloat(JSON.stringify(data['lat_b']));
      long_b = parseFloat(JSON.stringify(data['long_b']));
      lat_c = parseFloat(JSON.stringify(data['lat_c']));
      long_c = parseFloat(JSON.stringify(data['long_c']));
      lat_d = parseFloat(JSON.stringify(data['lat_d']));
      long_d = parseFloat(JSON.stringify(data['long_d']));
      lat_e = parseFloat(JSON.stringify(data['lat_e']));
      long_e = parseFloat(JSON.stringify(data['long_e']));
      lat_f = parseFloat(JSON.stringify(data['lat_f']));
      long_f = parseFloat(JSON.stringify(data['long_f']));
      origin = JSON.stringify(data['origin']).replace(/['"]+/g, '');
      destination = JSON.stringify(data['destination']).replace(/['"]+/g, '');
      directions = JSON.stringify(data['directions']);
      document.getElementById('duracion').innerHTML = JSON.stringify(data['directions']['duration']).replace(/['"]+/g, '').replace("minutes","minutos").replace("and","y").replace("seconds","segundos");
      document.getElementById('distancia').innerHTML = JSON.stringify(data['directions']['distance']).replace(/['"]+/g, '');
      if (repeat == true) {
        initMap()
        reload(); 
      }
    },
    error: function(error) {
      Error = error['responseJSON']
      console.log(Error)
      reload();
    }
  });
},5000);
}
reload();