
function changeTerm() {
    $('form').submit();
};

function courseAction(action){
  courseID = action.id;
  if (action.value == "Review"){
    reviewCourses(courseID)
  }
  else if (action.value == "View"){
    location = '/serviceLearning/viewProposal/' + courseID
  }
  else if (action.value == "Edit"){
    location = '/serviceLearning/editProposal/' + courseID
  }
}

function formSubmit(el) {
  $("#termSelector").attr('action', '/manageServiceLearning/' + el);
  $("#termSelector").submit()
};

function reviewCourses(action) {
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
    url: '/serviceLearning/approveCourse',
    type: "POST",
    data: {"courseID":courseID},
    success: function(){
      location.reload()
    }
  })
}

function unapproveProposal(el){
  let courseId = $(el).data("id")
  $.ajax({
    url: '/serviceLearning/unapproveCourse',
    type: "POST",
    data: {"courseID":courseID},
    success: function(){
      location.reload()
    }
  })
}
