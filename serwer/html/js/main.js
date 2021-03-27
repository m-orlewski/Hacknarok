var statusInterval;

function makeid(length) {
  var result           = '';
  var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var charactersLength = characters.length;
  for ( var i = 0; i < length; i++ ) {
     result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

$(document).ready(function() {
  // $(".reserve_form_form").hide();

  if(document.cookie.length == 0) {
    document.cookie = makeid(30);
  }
  console.log( document.cookie );

  fetch(`/status`)
  .then(res => res.text())
  .then(data => {
      if(data != 0) {
        statusInterval = window.setInterval(getStatus, 500);
        $('#myLargeModalLabel').modal('toggle')
      }
  });   

});

  $('#searchLocationBar').on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $(".card").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });

  $('.reserve-slot').click(function() {
    const id = $(this).attr('point_to');
    const name = $(`#${id} .card-title`).text();  
    var request = $.ajax({
      url: "reserve",
      method: "POST",
      data: { location_id:id,
              cookie:document.cookie
            },
    })


  //Kiedy zapytanie jest poprawne
  request.done(function( data ) {
      console.log(data);
      $("#alert-div").append('<div class="alert alert-success" role="alert">Zostałeś dodany do kolejki!</div>');
      // Constantly ask the databse for new messages
      statusInterval = window.setInterval(getStatus, 500);

  });
  
  //Blad w zapytaniu
  request.fail(function( jqXHR, textStatus ) {
      $("#alert-div").append('<div class="alert alert-danger" role="alert">Błąd podczas zapytania!</div>');
  });

  $('#myLargeModalLabel').modal('toggle')
  
  });



function getStatus() {
    fetch(`/status`)
    .then(res => res.text())
    .then(data => {
        data = JSON.parse(data);
        if( data[1] == 1 ) {
          $("#que-status").text(`Jesteś ${data[1]} w kolejce`);
        }
        else {
          $("#que-status").text(`Jesteś ${data[1]} w kolejce`);
        }
        return data
    });   
}


$(".cancel_slot").click(function() {
  fetch(`/cancel`)
    .then(res => res.text())
    .then(data => {
        clearInterval(statusInterval);
        $('#myLargeModalLabel').modal('toggle')

    });   
});