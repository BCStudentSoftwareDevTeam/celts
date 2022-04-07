import searchUser from './searchUser.js'

$(document).ready(function() {
  var table =  $('#trackVolunteerstable').DataTable({
  "fnDrawCallback": function(oSettings) {
    if ($('#trackVolunteerstable tr').length < 11) {
        $('.dataTables_paginate').hide(); //disable search and page numbers when the length of the table is less 11
        $('.dataTables_filter').hide();
        $('.dataTables_length').hide();
      }
    }
  });

  var table =  $('#trackOutsideParticipants').DataTable({
  "fnDrawCallback": function(oSettings) {
    if ($('#trackOutsideParticipants tr').length < 11) {
        $('.dataTables_paginate').hide(); //disable search and page numbers when the length of the table is less 11
        $('.dataTables_filter').hide();
        $('.dataTables_length').hide();
      }

   }
 });
});


$(".form-check-input").change(function updateMatch(el){
  let outsidePart =  $(this).attr('id');
  let volunteer = $(this).attr('name');
  let eventId = $("#eventID").val();
  var url = `/matchParticipants`
  if ($(this).attr('checked') == 'checked'){
   url = `/unMatch`
  }
  var matchData = {
    volunteer:volunteer,
    outsideParticipant:outsidePart,
    eventId:eventId,
  }

  $.ajax({
    url: url,
    type: "POST",
    data: matchData,
    success: function(s){
      location.reload();
    },
    error: function(request, status, error){
      location.reload();
    }
  })
});

  $('[data-toggle="tooltip"]').tooltip();
// Search functionalities from the volunteer table in the UI
  $("#trackVolunteersInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#volunteerTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });


function callback() {
  $("#selectVolunteerButton").prop('disabled', false);
}

$("#selectVolunteerButton").prop('disabled', true)

$("#addVolunteerInput").on("input", function() {
   console.log(addVolunteerInput,"this............");
  searchUser("addVolunteerInput", callback, "","addVolunteerModal");
  console.log(addVolunteerInput,"that...................");

});


$("#addOutsideParticipantButton").on("click",function(){
  $('#addVolunteerInput').id = "addOutsideParticipantInput";
  console.log($('addOutsideParticipantInput').val);
  console.log("The button transformation");
});


$(".removeVolunteer").on("click", function() {
  let username =  $(this)[0].id;
  let eventId = $('#eventID').val()
  $.ajax({
    url: `/removeVolunteerFromEvent/${username}/${eventId}`,
    type: "POST",
    success: function(s) {
      location.reload();
    },
    error: function(request, status, error) {
    }
  });
});

$(".removeParticipant").on("click", function() {
  let username =  $(this)[0].id;
  let eventId = $('#eventID').val()
  $.ajax({
    url: `/removeOutsideParticipantFromEvent/${username}/${eventId}`,
    type: "POST",
    success: function(s) {
      location.reload();
    },
    error: function(request, status, error) {
    }
  });
});

$(".attendanceCheck").on("change", function() {
  let username =  $(this)[0].name.substring(9) //get everything after the 9th character;
  let inputFieldID = `inputHours_${username}`

  if ($(this)[0].checked) {
    $(`#${inputFieldID}`).prop('disabled', false);
    let eventLength = $("#eventLength").text();
    $(`#${inputFieldID}`).val(eventLength);

  } else {
    $(`#${inputFieldID}`).prop('disabled', true);
    $(`#${inputFieldID}`).val(null);
  }
});

// WE HAVE TO MERGE THE FOLLOWING CODE BLOCLK ############################################
// Adding the new volunteer to the user database table
$("#selectVolunteerButton").click(function(){
  let user = $("#addVolunteerInput").val()
  let eventId = $("#eventID").val()

  $.ajax({
    url: `/addVolunteerToEvent/${user}/${eventId}`,
    type: "POST",
    success: function(s){
      location.reload();
    },
    error: function(request, status, error){
      location.reload();
    }
  });
});

// Addding an outside Participant
$("#selectParticipantButton").click(function(){
  let outsideParticipant = $("#addOutsideParticipantInput").val()
  let eventId = $("#eventID").val()

  $.ajax({
    url: `/addOutsideParticipantToEvent/${outsideParticipant}/${eventId}`,
    type: "POST",
    success: function(s){
      location.reload();
    },
    error: function(request, status, error){
      location.reload();
    }
  });
});




 // END OF THE CODE BLOCKES TO MBE MERGED.

//changing modals functions
function callback2() {
  $("#selectParticipantButton").prop('disabled', false);
}

$("#selectParticipantButton").prop('disabled', true)

$("#addOutsideParticipantInput").on("input", function() {
  console.log("This function is called");
  searchUser("addOutsideParticipantInput", callback2,"outsideParticipant", "addOutsideParticipantModal");
});
