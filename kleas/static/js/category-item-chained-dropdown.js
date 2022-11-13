$("#category-dropdown").change(function () {
    var url = $("#saleForm").attr("data-items-url");  // get the url of the `load_items` view
    var categoryId = $(this).val();                   // get the selected category ID from the HTML input

    $.ajax({                                          // initialize an AJAX request
      url: url,                                       // set the url of the request (= localhost:8000/hr/ajax/load-items/)
      data: {
        'category': categoryId                        // add the category id to the GET parameters
      },
      success: function (data) {                      // `data` is the return of the `load_items' view function
        $("#item-dropdown").html(data);
        $("#item-dropdown").selectpicker('refresh');             // replace the contents of the items input with the data that came from the server
      }
    });

});