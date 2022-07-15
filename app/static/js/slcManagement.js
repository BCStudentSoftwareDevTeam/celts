$(document).ready(function() {
  // if they decide not to withdraw, change selection back to "select action"
  $('#withdrawModal').on('hidden.bs.modal', function () {
    $('.form-select').val('---');
  });
  $("#withdrawBtn").on("click", function() {
    withdraw();
  });
  $('#renewBtn').click(function() {
    renew()
  });
});

function changeAction(action){
  courseID = action.id;
  // decides what to do based on selection
  if (action.value=="Renew"){
    $('#courseID').val(courseID);
    $("#renewModal").modal('show')
  } else if (action.value=="View"){
    // View
  } else if (action.value=="Withdraw"){
    $('#courseID').val(courseID);
    $('#withdrawModal').modal('show');
  } else if(action.value=="Edit"){
    location = '/serviceLearning/editProposal/' + courseID;
  }
}
function renew(course, term){
    courseID = $("#courseID").val();
    termID = $('#renewCourse').find(":selected").val()
    $.ajax({
      url: `/serviceLearning/renew/${courseID}/${termID}/`,
      type: "POST",
      success: function(s){
        location.reload();
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
