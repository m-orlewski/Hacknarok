
$("#create-location").click(function () {
    const nazwa_sklepu  = $("#nazwa_sklepu").val();
    const adres_sklepu  = $("#adres_sklepu").val();
    const powierzchnia  = $("#powierzchnia").val();

    console.log(nazwa_sklepu, adres_sklepu, powierzchnia);
    

    var request = $.ajax({
        url: "create",
        method: "POST",
        data: { nazwa_sklepu:nazwa_sklepu,
                adres_sklepu:adres_sklepu,
                powierzchnia:powierzchnia
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


  });