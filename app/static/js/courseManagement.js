function changeTerm() {
    $('form').submit();
};

function formSubmit(el) {
  $("#termSelector").attr('action', '/manageServiceLearning/' + el);
  $("#termSelector").submit()
};

function reviewCourses() { console.log("hdsvsdbvzk")
  $("#myReview").modal('show')
}
