
function changeTerm() {
    $('form').submit();
};

function formSubmit(el) {
  $("#termSelector").attr('action', '/manageServiceLearning/' + el);
  $("#termSelector").submit()
};

function reviewCourses(el) {
  let courseID = $(el).data('id');
  $.ajax({
    url: "/proposalReview/",
    type: "POST",
    data: {"course_id":courseID},
    success: function(modal_html) {
      $("#review-modal").html(modal_html)
      $("#proposal_view").modal('show')
    }
  })
}

function approveProposal(el){
  let courseID = $(el).data("id")
  $.ajax({
    url: '/serviceLearning/approveCourse/',
    type: "POST",
    data: {"courseID":courseID},
    success: function(){
      location.reload()
    }
  })
}
