function search(){
  if (!$('#searchbar').val())
    return;
  
  $.ajax({
    type: "GET",
    url: "/search",
    data: $('#searchbar').serialize(),
    success: function(data){
      console.log( data );
      $('#description').text(data.description);
      initMap(data.location);
    }
  });
  
}

function initMap(coord) {
        var uluru = {lat: coord.lat, lng: coord.lng};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 15,
          center: uluru
        });
        var marker = new google.maps.Marker({
          position: uluru,
          map: map
        });
      }

$( "#searchbutton" ).bind( "click", search);