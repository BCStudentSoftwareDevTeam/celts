$( document ).ready(function() {
    $(".Volunteers").hide();
    $(".outsidepart").hide();
    changeCounter = [];
    $('#createParticipantBtn').prop('disabled', true);
});

$(document).ready(function(){
  $("#Outsearch").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#Partul li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      if(!value) {
        $(".outsidepart").hide();
      }
      });
    });
  });

$(document).ready(function(){
  $("#Volsearch").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#Volul li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      if(!value) {
        $(".Volunteers").hide();
      }
    });
  });
});

function addResult(){
  console.log("Added!")
}

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
  $('#firstNameTextarea').val('').blur();
  $('#lastNameTextarea').val('').blur();
  $('#emailTextarea').val('').blur();
  $('#phoneNumberTextarea').val('').blur();
  changeCounter = [];
  $('#createParticipantBtn').prop('disabled', true);
  $.ajax({
    method: "POST",
    url: "/createParticipant",
    data: JSON.stringify(firstName, lastName, emailEntry, phoneNumber),
    contentType: "application/json",
    success: function(response) {
      print("Success")
    });
}

function checkForChange(input) {
  if (!changeCounter.includes(input)) {
    changeCounter.push(input);
  }
  if (changeCounter.length > 3) {
    $('#createParticipantBtn').prop('disabled', false);
  }
}
