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
 

$(document).ready(function() {
  $(document).on('click', '.remove_interested_student', function() {
      let username = $(this).attr('id'); 

      
      $.ajax({
          type: 'POST',
          url: '/profile/' + username + '/indicateInterest',
          success: function(response) {
            msgToast("Student successfully removed")
            location.reload();  
          },
          error: function(error) {
           console.log("error")
          }
      });
  });
});



$(document).ready(function() {
  $('#engagedStudentsTable').DataTable();
  $('#interestedStudentsTable').DataTable();
  $('#emailAllInterested').on('click', emailAllInterested);
});
