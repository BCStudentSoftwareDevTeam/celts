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


  $('[data-toggle="tooltip"]').tooltip();
  })
  $("pastVolunteers").on("click", function(){
    pastVolunteersButton();

 });
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

function callback() {
  $("#selectVolunteerButton").prop('disabled', false);
}

$("#selectVolunteerButton").prop('disabled', true)
$("#addVolunteerInput").on("input", function() {
  searchUser("addVolunteerInput", callback, false, "addVolunteerModal");
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

function pastVolunteersButton(){
  console.log("hello")
}
  // $.ajax({
  //   type: "POST",
  //   data: {recurringId: recurringId, startDate: startDate},
  //   success: function(jsonData) {
  //     var volunteerTable = $("#trackVolunteerstable")
  //     `/getPastVolunteer/${recurringId}/${startDate}`
  //     location.reload();
  //   }
  // });

// $.ajax({
//   type:"POST",
//   url: "/makeRecurringEvents",
//   data: eventDatesAndName, //get the startDate, endDate and name as a dictionary
//   success: function(jsonData){
//     var recurringEvents = JSON.parse(jsonData)
//     var recurringTable = $("#recurringEventsTable")
//     $("#recurringEventsTable tbody tr").remove();

//     for (var event of recurringEvents){
//       eventdate= new Date(event.date).toLocaleDateString()
//       recurringTable.append("<tr><td>"+event.name+"</td><td><input name='week"+event.week+"' type='hidden' value='"+eventdate+"'>"+eventdate+"</td></tr>");
//       }   
//   };

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
