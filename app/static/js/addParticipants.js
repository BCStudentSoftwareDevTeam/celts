
function searchVolunteer(){
  $("#volunteerInput").autocomplete({
    source: "/eventParticipants",
    minLength: 2,
  });
};


function addVolunteer(e){
  volunteersName = $(e).text()
  $("#Volunteertable").append('<tr><td>' + volunteersName + '</td><td><button id="removeButton" onclick="removeVolunteer(this)" type="button">x</button></td></tr>')
}

function removeParticipant(e) {
  var removeParticipant = $(this).attr("id")
  $("#"+removeParticipant).remove()
  $(e).parent().parent().remove();
}

function removeVolunteer(e) {
  $(e).parent().parent().remove();
}

count = 0;
function addOutsideParticipant() {
  firstName = $("#firstNameTextarea").val();
  lastName = $("#lastNameTextarea").val();
  emailEntry = $("#emailTextarea").val();
  phoneNumber = $("#phoneNumberTextarea").val();
  $("#OutsideTable").append('<tr id="removeRow"><td>' + firstName + " " + lastName + " " + '</td><td>' + emailEntry + " " +'</td><td>' + phoneNumber + " " + '</td><td><button id=' +count+ ' onclick="removeParticipant($(this))" type="button">x</button></td></tr>');
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
