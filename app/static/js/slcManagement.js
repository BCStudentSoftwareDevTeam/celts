$(document).ready(function() {
  // if they decide not to withdraw, change selection back to "select action"
  $('#withdrawModal').on('hidden.bs.modal', function () {
    $('.form-select').val('---');
  });
  $("#withdrawBtn").on("click", function() {
    withdraw();
  });
  var statusKey = $(".status-key");
  statusKey.popover({
    trigger: "hover",
    sanitize: false,
    html: true,
    content: function() {
      if ($(this).attr('data-content') == "Submitted") {
        return "This proposal has been submitted and is waiting on CELTS review."
      } else if ($(this).attr('data-content') == "Approved") {
        return "This proposal has been approved by CELTS."
      } else if ($(this).attr('data-content') == "In Progress") {
        return "This proposal has not been submitted for review."
      }
    }
  });
});

function updateRenewModal(courseID){
  // updates renewModal with the course's information
  $("#rMCourseNameCell").text($("#name-" + courseID).text())
  $("#rMFacultyCell").text($("#faculty-" + courseID).text())
  $("#rMStatusCell").text($("#status-" + courseID).text())
}
function changeAction(action){
  console.log(action)
  courseID = action.id;
  // decides what to do based on selection
  if (action.value == "Renew"){
    $('#courseID').val(courseID);
    updateRenewModal(courseID)
    $("#renewModal").modal('show')
  } else if (action.value == "View"){
    location = '/serviceLearning/viewProposal/' + courseID;
  } else if (action.value == "Withdraw"){
    $('#courseID').val(courseID);
    $('#withdrawModal').modal('show');
  } else if(action.value == "Edit"){
    location = '/serviceLearning/editProposal/' + courseID;
  } else if(action.value == "Print"){
    slcPrintPDF(courseID)
  } else if (action.value == "Review"){
    reviewCourses(courseID)
  }
}
function renew(){
    courseID = $("#courseID").val();
    termID = $('rMTermSelect').find(":selected").val()
    $.ajax({
      url: `/serviceLearning/renew/${courseID}/${termID}/`,
      type: "POST",
      success: function(newID){
        location = '/serviceLearning/editProposal/' + newID;
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
function slcPrintPDF(courseID){
  // KNOWN ISSUE: Firefox and Chrome load pages differently, due to this we had to add a timeout that as a hack workaround 
  // but it still has some issues. 
  var printProposal = window.open('/serviceLearning/print/' + courseID);
  setTimeout(function () {
            printProposal.print();
            var timeoutInterval = setInterval(function() {
              printProposal.close();
              // No clearing the interval on purpose becuase firefox needs it to repeat.
            }, 30);
        }, 100);
}

function changeTerm() {
  $('form').submit();
};

function formSubmit(el) {
$("#termSelector").attr('action', '/manageServiceLearning/' + el);
$("#termSelector").submit()
};

function reviewCourses(courseID) {
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
let courseID = $(el).data("id")
$.ajax({
  url: '/serviceLearning/unapproveCourse',
  type: "POST",
  data: {"courseID":courseID},
  success: function(){
    location.reload()
  }
})
}
