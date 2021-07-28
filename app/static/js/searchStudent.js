
// Search functionalities from the user table in the database
function searchStudents(){
  var query = $("#searchStudentsInput").val()

  $("#searchStudentsInput").autocomplete({
    minLength: 2,
    source: function(request, response){

      $.ajax({
        url: "/searchStudents/" + query,
        type: "GET",
        dataType: "json",
        success: function(dictToJSON) {
          response($.map( dictToJSON, function( item ) {
            return {
            label: item,
            value: dictToJSON[item]
            }
          }))
        },
        error: function(request, status, error) {
          console.log(status,error);
        }
      })
    },
     select: function(event , ui) {
       var user = ui.item.value
       username = user.split(" ")
       console.log(username[2].slice(1, -1))
       $("#searchStudentsInput").val(ui.item.value)
       $('#searchStudent').submit()

     }
  });
};
