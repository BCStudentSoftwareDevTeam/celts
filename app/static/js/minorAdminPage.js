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
 

function removeVolunteer(){
  $(".removeVolunteer").prop("disabled", true)
  let username =  this.id;
  let eventId = $('#eventID').val()
  $.ajax({
    url: '/removeVolunteerFromEvent',
    type: "POST",
    data: {username: username, eventId: eventId},
    success: function(response) {
       location.reload();
    },
    error: function(request, status, error) {
        $(".removeVolunteer").prop("disabled", false)
    }
  });
}


$(document).ready(function() {
  $('#engagedStudentsTable').DataTable();
  $('#interestedStudentsTable').DataTable();
  $('#emailAllInterested').on('click', emailAllInterested);
});
