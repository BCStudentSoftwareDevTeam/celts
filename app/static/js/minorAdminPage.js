import searchUser from './searchUser.js'
function emailAllInterested(){
  // Read all student emails from the input as a string and put them in mailto format
  let interestedStudentEmails =  $("#interestedStudentEmails").val();
  // If there are any students interested, open the mailto link
  if (interestedStudentEmails.length) {
    const windowRef = window.open(`mailto:${interestedStudentEmails}`, '_blank');
    windowRef.focus();
    setTimeout(function(){
      if(!windowRef.document) {
          windowRef.close();
      }
    }, 500);
  } else {
    msgFlash("No interested students to email.", "info")
  }
}


function getInterestedStudents() {
  // get all the checkboxes and return a list of users who's
  // checkboxes are selected
  let checkboxesDisplayedInModal = $("#addInterestedStudentsModal input[type=checkbox]")
  let interestedStudentsList = []
   checkboxesDisplayedInModal.each(function(index, checkbox){
    if(checkbox["checked"]){
      interestedStudentsList.push(checkbox["value"])
    }
  })
  return interestedStudentsList
}

function updateInterestedStudents(){
  let interestedStudentList = getInterestedStudents()
  let buttonContent = $("#addInterestedStudentsbtn").html()
  if (interestedStudentList.length > 1) {
    if (buttonContent.charAt(buttonContent.length-1) != "s") {
      // make the button text plural if there are multiple users selected
      $("#addInterestedStudentsbtn").html(buttonContent + "s")
    }
  } else if (buttonContent.charAt(buttonContent.length-1) == "s") {
    // remove the s if it is plural and we have less than 2 volunteers
    $("#addInterestedStudentsbtn").html(buttonContent.slice(0, -1))
  }
  // disable the submit button if there are no selectedCheckboxes
  if (interestedStudentList.length == 0) {
   
    $("#addInterestedStudentsbtn").prop("disabled", true)
  } else {
    $("#addInterestedStudentsbtn").prop("disabled", false)
  }
  $('#addInterestedStudentsbtn').click(function() {
    $('#interestedStudentForm').submit();s
  });
}


var userlist = $(".interestedStudentList").map(function(){
  return $(this).val()
}).get()
function callback(selected) {
  let user = $("#addStudentInput").val()
  if (userlist.includes(selected["username"]) == false){
      userlist.push(user)
      let i = userlist.length;
      $("#interestedStudentList").prepend("<li class id= 'interestedStudentElement"+i+"'> </li>")          
      $("#interestedStudentElement"+i).append("<input  name = 'interestedStudents[]' type='checkbox' id= 'userlistCheckbox"+i+"' checked value='" + user +"' >  </input> ")
      $("#interestedStudentElement"+i).append("<label form for= 'userlistCheckbox"+i+"'>"+ selected["firstName"]+ " " + selected["lastName"] +"</label>")
      //handleBanned(selected["username"], $("#eventID").val(), i)
      $("#userlistCheckbox"+i).click(updateInterestedStudents)
      updateInterestedStudents()
  }
  else {
      msgFlash("User already selected.")
  }
}
$("#addInterestedStudentsbtn").prop('disabled', true);
+
$("#addInterestedStudentsModal").on("shown.bs.modal", function() {
  $('#addStudentInput').focus();
});

$("#addStudentInput").on("input", function() {
searchUser("addStudentInput", callback, true, "addInterestedStudentsModal");
});



// function removeVolunteer(){
//   $(".removeVolunteer").prop("disabled", true)
//   let username =  this.id;
//   let eventId = $('#eventID').val()
//   $.ajax({
//     url: '/removeVolunteerFromEvent',
//     type: "POST",
//     data: {username: username, eventId: eventId},
//     success: function(response) {
//        location.reload();
//     },
//     error: function(request, status, error) {
//         $(".removeVolunteer").prop("disabled", false)
//     }
//   });
// }



$(document).ready(function() {
  $('#engagedStudentsTable').DataTable();
  $('#interestedStudentsTable').DataTable();
  $('#emailAllInterested').on('click', emailAllInterested);
});
