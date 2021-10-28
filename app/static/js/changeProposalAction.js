
// withdrawing a course

$(document).ready(function() {
  //if they decide not to withdraw, change selection back to "select action"
  $('#withdrawModal').on('hidden.bs.modal', function () {
    $('.form-select').val('---');
  });
  $("#withdrawBtn").on("click", function() {
    withdraw();
  });
  for (var i=1; i<=$('#proposalTable .form-select').length; i++){
    $("#course_"+i).on("change", function() {
      changeAction($(this));
    });
  }
});

function changeAction(action){
  if (action.value=="Renew"){
    // Renew

  } else if (action.value=="View"){
    // View

  } else if (action.value=="Withdraw"){
    courseID = action.id;
    console.log("hello");
    $('#courseToRemove').val(courseID);
    $('#withdrawModal').modal('show');

  } else if(action.value=="Edit"){
    // Edit
  }
}

function withdraw(){
  courseID = $("#courseToRemove").val()
  $.ajax({
    url: "/withdrawCourse/"+ courseID,
    type: "POST",
    success: function(s){
      location.reload()
    },
    error: function(request, status, error) {
        console.log(status,error);
      }
  })
};
