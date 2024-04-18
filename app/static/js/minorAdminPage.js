function emailAllInterested(){
  // Read all student emails from the input as a string and put them in mailto format
  let interestedStudentEmails = $("#interestedStudentEmails").val().slice(1, -1).replace(/['\s]/g, '')
  // If there are any students interested, open the mailto link
  if (interestedStudentEmails.length) {
    const windowRef = window.open(`mailto:${interestedStudentEmails}`, '_blank');
    windowRef.focus();
    setTimeout(function(){
      if(!windowRef.document) {
          windowRef.close();
      }
    }, 500);
  }
}

$(document).ready(function() {
  $('#engagedStudentsTable').DataTable();
  $('#interestedStudentsTable').DataTable({
    "fnDrawCallback": function(oSettings) {
      $('#interestedStudentsTable_wrapper .dataTables_length').html(`<button class="btn btn-primary" id="emailAllInterested">Email All</button>`);
      $('#emailAllInterested').on('click', emailAllInterested);
    }
  });
});
