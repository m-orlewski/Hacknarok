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
    // $(".reserve_form_form h3").text(`Rezerwuj miejsce w kolejce do ${name}`);
    // $("#reserve_id").val(id);
    // $(".reserve_form_form").fadeIn();
  // });

  // $(".reserve_form_form button").click(function() {
    // const name = $("#user_name").val();
    // const location_id = $("#reserve_id").val();

    // console.log(name, location_id);
  
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
      $("#alert-div").append('<div class="alert alert-success" role="alert">Dodano nową lokalizację!</div>');
  });
  
  //Blad w zapytaniu
  request.fail(function( jqXHR, textStatus ) {
      $("#alert-div").append('<div class="alert alert-danger" role="alert">Błąd podczas zapytania!</div>');
  });

  $('#myLargeModalLabel').modal('toggle')


  
  });