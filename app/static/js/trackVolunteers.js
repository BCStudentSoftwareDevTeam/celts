import searchUser from './searchUser.js'

$(document).ready( function () {
  // console.log(data['column'])
    $('#trackVolunteerstable').DataTable({
      "fnDrawCallback": function(oSettings) {
       if ($('#example tr').length < 11) {

           $('.dataTables_paginate').hide();
           
       }
   }

      // "lengthChange": false,
      // if (data ['row'] <= 10) {
      //     "searching": false,;
      // },
      // responsive: true
       // columnDefs: [
       //  { responsivePriority: 6 ,targets: 6},
       //  { responsivePriority: 5 ,targets: 5},
       //  { responsivePriority: 4 ,targets: 4},
       //  { responsivePriority: 3 ,targets: 3},
       //  { responsivePriority: 2 ,targets: 2},
       //  { responsivePriority: 1 ,targets: 1}



    // ]

    });
}
);

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
    url: "/addVolunteerToEvent/" + user+"/"+volunteerEventID+"/"+eventLengthInHours,
    type: "POST",
    success: function(s){
      location.reload();

    },
    error: function(request, status, error){
      location.reload();
      console.log(status,error);
    }
    })
  })
});

// Deleting a volunteer from the eventParticipant database table
function removeVolunteerFromEvent (deleteIcon){
  let user =  deleteIcon.id.substring(11)
  console.log(user)
  let eventID = $('#eventID').val()
  $.ajax({
    url: "/removeVolunteerFromEvent/"+ user +"/"+ eventID,
    type: "POST",
    success: function(s){
      location.reload()

    },
    error: function(request, status, error) {
        console.log(status,error);
      }
  })
}

function callback() {
  $("#selectVolunteerButton").prop('disabled', false);
}

$("#selectVolunteerButton").prop('disabled', true)
$("#addVolunteerInput").on("input", function() {
  searchUser("addVolunteerInput", callback, "addVolunteerModal");
});

function toggleVolunteersInputBox(checkbox) {
  let username =  checkbox.id.substring(9) //get everything after the 9th character
  let inputFieldID = 'inputHours_'+username

  if (checkbox.checked) {
    console.log($('#'+inputFieldID).val())
    $('#'+inputFieldID).prop('readonly', false)

    let eventLength = $("#eventLength").text()
    $('#'+inputFieldID).val(eventLength)

  } else {
    $('#'+inputFieldID).prop('readonly', true)
    $('#'+inputFieldID).val('')
  }
 }
