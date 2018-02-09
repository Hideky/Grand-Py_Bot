function search(){
  if (!$('#searchbar').val())
    return;
  
  // Save actual status to backup after search
  searchButton = $('#searchbutton')
  $('#searchbutton').html('<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span> Je réfléchi...')

  $.ajax({
    type: "GET",
    url: "/search",
    data: $('#searchbar').serialize(),
    success: function(data){
      $('#status').text("Je me souviens d'une histoire à ce propos...");
      $('#description').text(data.description);
      initMap(data.location);
    },
    error: function(){
      $('#status').text("Malheureusement, je ne connais aucune histoire à ce propos...");
      $('#description,#map').empty()
    },
    complete: function(){
      $('#searchbutton').text("Raconte moi une autre histoire")
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

$('#searchbutton').bind( "click", search);
$('#searchbar').bind('keydown', function (k) {
    if (k.keyCode == 13) {
        $('#searchbutton').click();
    }
});