$( document ).ready(function() {
    $(".Volunteers").hide();
    $(".outsidepart").hide();

});

function removeParticipants(btn) {

  var row = btn.parent().parent();
  row.parent().removeChild(row);
}

function removeVolunteer(btn) {

  var row = btn.parent().parent();
  row.parent().removeChild(row);

}

function textboxValue() {
firstName = $("#firstNameTextarea").val();
lastName = $("#lastNameTextarea").val();
emailEntry = $("#emailTextarea").val();
phoneNumber = $("#phoneNumberTextarea").val();
console.log(firstName)
console.log(phoneNumber)
// $("#OutsideTable").append('<tr><td>{{ firstName + "" + lastName }}</td><td>{{ emailEntry }}</td> <td>{{ phoneNumber }}</td><td><button onclick="removeParticipants(this)" type="button">x</button></td></tr>');
}
