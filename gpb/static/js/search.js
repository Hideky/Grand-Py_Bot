function search(){
  if (!$('#searchbar').val())
    return;
  
  // Save actual status to backup after search
  searchButton = $('#searchbutton')

  // Change button when searching
  $('#searchbutton').html('<span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span> Je réfléchi...')
  $('#searchbutton').prop('disabled', true);

  $.ajax({
    type: "GET",
    url: "/search",
    data: $('#searchbar').serialize(),
    success: function(data){
      $('#status').text("Je me souviens d'une histoire à ce propos...");
      // Show map and description
      $('#description').text(data.description);
      initMap(data.location);
    },
    error: function(){
      $('#status').text("Malheureusement, je ne connais aucune histoire à ce propos...");
      // Clear map and description when no response
      $('#description,#map').empty()
    },
    complete: function(){
      // Revert button changing when searching
      $('#searchbutton').text("Raconte moi une autre histoire")
      $('#searchbutton').prop('disabled', false);
    }
  });
  
}

// Function used to set a new google map (export from google map api doc)
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

// Binding of Enter on search bar
$('#searchbutton').bind( "click", search);
$('#searchbar').bind('keydown', function (k) {
    if (k.keyCode == 13) {
        $('#searchbutton').click();
    }
});