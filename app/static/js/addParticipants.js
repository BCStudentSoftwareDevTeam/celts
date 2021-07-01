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
  // var $row = $(e);
  //console.log($row.find(':nth-child(2)').text());
  // console.log($(e).parent().parent()[0].(document).text("td:nth-child(2)"));
  text = $(e).parent().parent()[0].textContent;
  text2 = JSON.stringify(text);
  console.log(text2);
  $.ajax({
    method: "POST",
    url: "/removeParticipant",
    data: text2,
    contentType: "application/json; charset=utf-8",
    success: function(response) {
      console.log("Success");
    },
    error: function(request, status, error) {
      console.log(status,error);
    }
  });
  $(e).parent().parent().remove();
}

function removeVolunteer(e) {
  $(e).parent().parent().remove();
}

function textboxValue() {
  var formValues = {
      event: "2",
      firstName: $("#firstNameTextarea").val(),
      lastName: $("#lastNameTextarea").val(),
      emailEntry: $("#emailTextarea").val(),
      phoneNumber: $("#phoneNumberTextarea").val(),
    };
  changeCounter = [];
  $('#createParticipantBtn').prop('disabled', true);
  var formStringified = JSON.stringify(formValues, null, 2);
  $.ajax({
    method: "POST",
    url: "/createParticipant",
    data: formStringified,
    contentType: "application/json; charset=utf-8",
    success: function(response) {
      console.log("Success");
    },
    error: function(request, status, error) {
      console.log(status,error);
    }
  });

  firstName = $("#firstNameTextarea").val();
  lastName = $("#lastNameTextarea").val();
  emailEntry = $("#emailTextarea").val();
  phoneNumber = $("#phoneNumberTextarea").val();
  $("#OutsideTable").append('<tr id="removeRow"><td>' + firstName + " " + lastName + " " + '</td><td>' + emailEntry + " " +'</td><td>' + phoneNumber + " " + '</td><td><button id="removeButton" onclick="removeParticipants(this)" type="button">x</button></td></tr>');
  $('#firstNameTextarea').val('').blur();
  $('#lastNameTextarea').val('').blur();
  $('#emailTextarea').val('').blur();
  $('#phoneNumberTextarea').val('').blur();
};

function checkForChange(input) {
  if (!changeCounter.includes(input)) {
    changeCounter.push(input);
  }
  if (changeCounter.length > 3) {
    $('#createParticipantBtn').prop('disabled', false);
  }
}
