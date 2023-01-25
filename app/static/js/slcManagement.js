$(document).ready(function() {
  // if they decide not to withdraw, change selection back to "select action"
  $('#withdrawModal').on('hidden.bs.modal', function () {
    $('.form-select').val('---');
  });
  $("#withdrawBtn").on("click", function() {
    withdraw();
  });
});

function changeAction(action){
  courseID = action.id;
  // decides what to do based on selection
  if (action.value == "Renew"){
    $('#courseID').val(courseID);
    $("#course-" + courseID).modal('show')
  } else if (action.value == "View"){
    location = '/serviceLearning/viewProposal/' + courseID
  } else if (action.value == "Withdraw"){
    $('#courseID').val(courseID);
    $('#withdrawModal').modal('show');
  } else if(action.value == "Edit"){
    location = '/serviceLearning/editProposal/' + courseID;
  } else if(action.value == "Download"){
    slcDownloadPDF(courseID)
  }
}
function renew(){
    courseID = $("#courseID").val();
    termID = $('#renewCourse-'+courseID).find(":selected").val()
    $.ajax({
      url: `/serviceLearning/renew/${courseID}/${termID}/`,
      type: "POST",
      success: function(newID){
        location = '/serviceLearning/editProposal/' + newID;
      },
      error: function(request, status, error) {
          console.log(status,error);
      }
    })
}
function withdraw(){
  // uses hidden label to withdraw course
  courseID = $("#courseID").val();
  $.ajax({
    url: `/serviceLearning/withdraw/${courseID}`,
    type: "POST",
    success: function(s){
      location.reload();
    },
    error: function(request, status, error) {
        console.log(status,error);
    }
  })
};
function slcDownloadPDF(courseID){
  $.ajax({
    url: `/serviceLearning/download/${courseID}`,
    type: "GET",
    success: function(response){
      var doc = new jsPDF('portrait', 'pt', 'letter');
      margins = {
             top: 40,
             bottom: 60,
             left: 40,
             width: 522
             };
       doc.fromHTML(response, margins.left,margins.top, {width: margins.width}); // Change the HTML template to PDF
      doc.save()
    }
  })
}
