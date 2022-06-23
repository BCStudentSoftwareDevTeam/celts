function changeTerm() {
    $('form').submit();
};

function formSubmit(el) {
  $("#termSelector").attr('action', '/manageServiceLearning/' + el);
  $("#termSelector").submit()
}
function openForm() {
  $("#myForm").modal("toggle");
}

function addInstructorS() {
  console.log("We're here");
  $.ajax({
    method: "POST",
    url:  "/addInstructor",
    data: {"username": $("#uname").val(),
           "bnumber":$("#bnum").val(),
           "email":$("#email").val(),
           "phoneNumber":$("#pnum").val(),
           "firstName":$("#fname").val(),
           "lastName":$("#lname").val()
          },
    success: function(response) {

      location.reload();
    }
  });
}
