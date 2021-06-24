$( document ).ready(function() {
    $(".Volunteers").hide();
    $(".outsidepart").hide();

});

function removeParticipants(e) {

  $(e).parent().parent().remove();
}

function removeVolunteer(e) {

  $(e).parent().parent().remove();
}

function textboxValue() {
firstName = $("#firstNameTextarea").val();
lastName = $("#lastNameTextarea").val();
emailEntry = $("#emailTextarea").val();
phoneNumber = $("#phoneNumberTextarea").val();
$("#OutsideTable").append('<tr id="removeRow"><td>' + firstName + " " + lastName + " " + '</td><td>' + emailEntry + " " +'</td><td>' + phoneNumber + " " + '</td><td><button id="removeButton" onclick="removeParticipants(this)" type="button">x</button></td></tr>');
}
