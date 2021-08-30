
function searchInstructor(){
var query = $("#instructorInput").val()
$("#instructorInput").autocomplete({
  minLength: 2,
  source: function(request, response){
    $.ajax({
      url: "/searchInstructor/" + query,
      type: "GET",
      contentType: "application/json",
      data: query,
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
  select: function( event, ui ) {
    var instructorName = ui.item.value
    $("#instructorTable").append('<tr><td>' + instructorName + '</td><td><button id="removeButton" onclick="removeRow(this)" type="button"><i class="bi bi-trash" style="font-size:20px"></i></button></td></tr>');
    $("#instructorInput").val(''); return false;

    }
  });
};


function removeRow(e) {
  $(e).parent().parent().remove();
}
