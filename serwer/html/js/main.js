
  $('#searchLocationBar').on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $(".card").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });


  $('.reserve-slot').click(function() {
    const id = $(this).attr('point_to');
    const name = $(`#${id} .card-title`).text();

    $(".reserve_form_button h3").text(`Rezerwuj miejsce w kolejce do ${name}`);
    $("#reserve_id").val(id);
  });