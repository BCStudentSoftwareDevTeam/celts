function changeTerm() {
    $('form').submit();
};

function formSubmit(el) {
  $("#termSelector").attr('action', '/manageServiceLearning/' + el);
  $("#termSelector").submit()
}

function addInstructorS() {
  console.log("We're here");
  $.ajax({
    method: "POST",
    url:  "/addInstructor",
    data: {"username": $("#uname").val(),
          },
    success: function(response) {

      location.reload();
    }
  });
}
