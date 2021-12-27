import searchUser from './searchUser.js'
import searchOutsideParticipant from './searchOutsideParticipant.js'

$(document).ready( function () {
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
    if ($('#trackVolunteerstable tr').length < 11) {
        $('.dataTables_paginate').hide(); //disable search and page numbers when the length of the table is less 11
        $('.dataTables_filter').hide();
        $('.dataTables_length').hide();
      }

   }
 });
 var currentVolunteer = "";
 $(document).on("click", ".open-MatchDialog", function () {
      currentVolunteer = $(this).data('id');
      $(".matchModalBody #selectionId").val( currentVolunteer );
 });

 $(".form-check-input").click(function updateMatch(el){
   let currID =  $(this).attr('id');
   let user = $(this).attr('name');
   let eventId = $("#eventID").val()

   $.ajax({
     url: `/matchParticipants/${currentVolunteer}/${currID}/${eventId}`,
     type: "POST",
     success: function(s){
       // location.reload();
     },
     error: function(request, status, error){
       // location.reload();
     }
   });

 });

});

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
    let participant = $("#addOutsideParticipantInput").val()
    let eventId = $("#eventID").val()

    $.ajax({
      url: `/addParticipantToEvent/${participant}/${eventId}`,
      type: "POST",
      success: function(s){
        location.reload();
      },
      error: function(request, status, error){
        location.reload();
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
    url: `/removeParticipantFromEvent/${username}/${eventId}`,
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
    $(`#${inputFieldID}`).prop('readonly', false);
    let eventLength = $("#eventLength").text();
    $(`#${inputFieldID}`).val(eventLength);

  } else {
    $(`#${inputFieldID}`).prop('readonly', true);
    $(`#${inputFieldID}`).val(null);
  }
});


function callback2() {
  $("#selectParticipantButton").prop('disabled', false);
}

$("#selectParticipantButton").prop('disabled', true)

$("#addOutsideParticipantInput").on("input", function() {
  searchOutsideParticipant("addOutsideParticipantInput", callback2, "addOutsideParticipantModal");
});

$("#doneMatching").on("click",function(){
  location.reload()
})
