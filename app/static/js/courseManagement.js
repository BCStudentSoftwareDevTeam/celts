function changeTerm() {
    $('form').submit();
};

function formSubmit(el) {
  $("#termSelector").attr('action', '/manageServiceLearning/' + el);
  $("#termSelector").submit()
};

function reviewCourses(el) {
  $("#myReview").modal('show')
  var courseID=$(el).attr('data-id');
  console.log(courseID)
  $.ajax({
    url:"/proposalReview/",
    type:"POST",
    data:{"course_id":courseID},
    success: function(course_data) {
      $("div").append(course_data)
      

    }
  })
}
