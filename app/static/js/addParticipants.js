function searchVolunteer(){
var query = $("#volunteerInput").val()
$("#volunteerInput").autocomplete({
  minLength: 2,
  source: function(request, response){
    $.ajax({
      url: "/searchStudents/" + query,
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
    var volunteerName = ui.item.value
    $("#Volunteertable").append('<tr><td>' + volunteerName + '</td><td><button id="removeButton" onclick="removeRow(this)" type="button">x</button></td></tr>')

    }
  });
};
function removeRow(e) {
  $(e).parent().parent().remove();
}

count = 0;
function addOutsideParticipant() {
  firstName = $("#firstNameTextarea").val();
  lastName = $("#lastNameTextarea").val();
  emailEntry = $("#emailTextarea").val();
  phoneNumber = $("#phoneNumberTextarea").val();
  $("#OutsideTable").append('<tr id="removeRow"><td>' + firstName + " " + lastName + " " + '</td><td>' + emailEntry + " " +'</td><td>' + phoneNumber + " " + '</td><td><button id=' +count+ ' onclick="removeRow($(this))" type="button">x</button></td></tr>');
  opList = ["email", "firstName", "lastName", "phoneNumber"];
  opList.forEach(item => {
    $("<input type='text' hidden/>")
    .attr("value", $('#'+item+'Textarea').val())
    .attr("id", item+count)
    .attr("name", item+count)
    .appendTo("#"+count)
    $('#'+item+'Textarea').val('').blur();
  })
  count++;
  $('#particpantsModal').modal('hide')
}
