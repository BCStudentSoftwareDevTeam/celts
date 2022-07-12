
function changeTerm() {
    $('form').submit();
};

function formSubmit(el) {
  $("#termSelector").attr('action', '/manageServiceLearning/' + el);
  $("#termSelector").submit()
};

function reviewCourses(el) {
  var courseID=$(el).attr('data-id');
  $.ajax({
    url:"/proposalReview/",
    type:"POST",
    data:{"course_id":courseID},
    success: function(modal_html) {
      $("#review-modal").html(modal_html)
      $("#proposal_view").modal('show')
    }
  })
}

function approve_proposal(el){
  var courseID=$(el).attr('course-id');
  $.ajax({
    url:'/serviceLearning/approveCourse/',
    type:"POST",
    data:{"course_id":courseID},
    success: function(){
      location.reload()
    }  
  })
}
