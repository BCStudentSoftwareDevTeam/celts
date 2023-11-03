$(document).ready(function() {
  // if they decide not to withdraw, change selection back to "select action"
  $('.modal').on('hidden.bs.modal', function () {
    resetAllSelections()
  });
  $('#renewTerm').on('change', function(){
    if ($('#renewTerm').value != "---"){
      $('#renewBtn').prop('disabled', false);
    }
  });
  $("#withdrawBtn").on("click", withdraw);
  $("#renewBtn").on("click", renew);
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


function resetAllSelections(){
  $('.form-select').val('---');
  $('#renewBtn').prop('disabled', true);
}
function updateRenewModal(courseID){
  // updates renewModal with the course's information
  $("#renewName").text($("#name-" + courseID).text())
  $("#renewFaculty").text($("#faculty-" + courseID).text())
  $("#renewStatus").text($("#status-" + courseID).text())
}
function changeAction(action){
  courseID = action.id;
  courseAction = action.value
  // decides what to do based on selection
  if (courseAction == "Renew"){
    $('#courseID').val(courseID);
    updateRenewModal(courseID)
    $("#renewModal").modal('show')
  } else if (courseAction == "View"){
    location = '/serviceLearning/viewProposal/' + courseID;
  } else if (courseAction == "Withdraw"){
    $('#courseID').val(courseID);
    $('#withdrawModal').modal('show');
  } else if(courseAction == "Edit"){
    location = '/serviceLearning/editProposal/' + courseID;
  } else if (courseAction == "Alter"){
    $('#courseID').val(courseID);
    showImportedCourseModal();
  } else if(courseAction == "Print"){
    slcPrintPDF(courseID)
  } else if (courseAction == "Review"){
    reviewCourses(courseID)
  }
  // leave these two selected until the modal is closed
  if (courseAction != "Renew" && courseAction != "Withdraw"){
    resetAllSelections()
  }
}
function renew(){
    courseID = $("#courseID").val();
    termID = $('#renewTerm').find(":selected").val()
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
    resetAllSelections()
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


function getImportedCourseInfo(callback){
  courseID = $("#courseID").val();
  $.ajax({
    url: `/manageServiceLearning/imported/${courseID}`,
    type: "GET",
    success: function(data) { 
      // Takes in a list of length 2. First element is the courseDict and the second is a list of instructors 
      if (Object.keys(data).length != 2){
        callback();
        return;
      }
      var courseData = data.courseData;
      var courseInstructors = data.courseInstructors;
      if (Object.keys(courseData).length !== 0){
        // update the alter imported course modal
        $('#courseName').val(courseData['courseName']);
        $('#courseAbbreviation').val(courseData['courseAbbreviation']);
        $('#courseCredit').val(courseData['courseCredit']);
      }  
      var htmlInstructorRows = "";
      var instructorTableNameInputs = "";
      for (let instructor of courseInstructors){
        htmlInstructorRows += `
            <tr data-username='${instructor.username}'>
              <td>
                <p class='mb-0'> ${instructor.firstName} ${instructor.lastName} (${instructor.email})</p>
                  <input type='text' style='border: none' size='14' class='form-control-sm' id='inputPhoneNumber-${instructor.username}' name='courseInstructorPhone' aria-label='Instructor Phone' data-value='${instructor.phoneNumber}' value='${instructor.phoneNumber}' placeholder='Phone Number' />
                  <a class='text-decoration-none primary editButton' tabindex='0' data-username='${instructor.username}' id='editButton-${instructor.username}' type='button'>Edit</a>
              </td>
              <td class='align-middle'>
                  <button id='remove' type='button' class='btn btn-danger removeButton'>Remove</button>
              </td>
            </tr>`
        instructorTableNameInputs += `<input hidden name="instructor[]" value='${instructor.username}'/>`
      }
      $("#instructorTableBody").html(htmlInstructorRows);
      $("#instructorTableNames").html(instructorTableNameInputs);
      $("#instructorTableBody .removeButton").off("click");
      $("#instructorTableBody .removeButton").on("click", function(){
          let closestRow =  $(this).closest("tr")
          $("#instructorTableNames input[value="+closestRow.data('username')+"]").remove()
          closestRow.remove();
      });

      callback();
      
    }
  })
}

function showImportedCourseModal(){
  getImportedCourseInfo(function(){  // Since ajax calls send immediately we need following actions called as a callback
    $('#alterModal').modal('show'); 
  });
}


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
