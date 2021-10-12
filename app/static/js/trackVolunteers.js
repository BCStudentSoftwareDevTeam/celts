import searchUser from './searchUser.js'

$(document).ready(function() {
  $('[data-bs-toggle="tooltip"]').tooltip();
// Search functionalities from the volunteer table in the UI
  $("#trackVolunteersInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#volunteerTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

  // Adding the new volunteer to the user database table
  $("#selectVolunteerButton").click(function(){
    let user = $("#addVolunteerInput").val()
    let volunteerEventID = $("#eventID").val()
    let eventLengthInHours = $("#eventLength").text()

    $.ajax({
      url: `/addVolunteerToEvent/${user}/${volunteerEventID}/${eventLengthInHours}`,
      type: "POST",
      success: function(s){
        location.reload();
      },
      error: function(request, status, error){
        location.reload();
        console.log(status,error);
      }
    });
  });
});

function callback() {
  $("#selectVolunteerButton").prop('disabled', false);
}

$("#selectVolunteerButton").prop('disabled', true)
$("#addVolunteerInput").on("input", function() {
  searchUser("addVolunteerInput", callback, "addVolunteerModal");
});

$(".removeVolunteer").on("click", function() {
  let username =  $(this)[0].id;
  let eventID = $('#eventID').val()
  $.ajax({
    url: `/removeVolunteerFromEvent/${username}/${eventID}`,
    type: "POST",
    success: function(s) {
      location.reload();
    },
    error: function(request, status, error) {
      console.log(status, error);
    }
  });
});

$(".attendanceCheck").on("change", function() {
  let username =  $(this)[0].value;
  let inputFieldID = `inputHours_${username}`

  if ($(this)[0].checked) {
    $(`#${inputFieldID}`).prop('readonly', false);
    let eventLength = $("#eventLength").text();
    $(`#${inputFieldID}`).val(eventLength);

  } else {
    $(`#${inputFieldID}`).prop('readonly', true);
    $(`#${inputFieldID}`).val('');
  }
});
