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
  // decides what to do based on selection
  if (action.value=="Renew"){
    // Renew

  } else if (action.value=="View"){
    // View

  } else if (action.value=="Withdraw"){
    courseID = action.id;
    $('#courseToRemove').val(courseID);
    $('#withdrawModal').modal('show');

  } else if(action.value=="Edit"){
    // Edit
  }
}

function withdraw(){
  // uses hidden label to withdraw course
  courseID = $("#courseToRemove").val()
  $.ajax({
    url: "/courseProposals/"+courseID+"/withdraw/",
    type: "POST",
    success: function(s){
      location.reload()
    },
    error: function(request, status, error) {
        console.log(status,error);
      }
  })
}
