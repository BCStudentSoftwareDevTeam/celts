import {getCourseInstructors, getRowUsername, createNewRow} from './instructorTable.js'
import searchUser from './searchUser.js';
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
  $("#alterModal").on("hide.bs.modal", emptyInstructorTable);
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

      } else if ($(this).attr('data-content') == "Imported") {
        return "This course has been imported and is waiting for review."

      }
    }
  });


  $("#instructorTable").on("click", ".removeButton", function() {
    $(this).closest("tr").find(".editButton").each(function() {
      let username = $(this).data('username');
  
      // Remove input with matching username value
      $("#instructorTableNames input[value='" + username + "']").remove();
  
      // Remove the closest tr
      $(this).closest("tr").remove();
    });
  });

  $("#courseInstructor").on('input', function() {
      searchUser("courseInstructor", createNewRow, true, null, "instructor");
      setTimeout(function() {
        $(".ui-autocomplete").css("z-index", 9999);
      }, 500);
  });

  // for each row in instructorTable that has an instructor, pass that instructors phone data to setupPhoneNumber
  $('#alterModal').on('shown.bs.modal', function () {
    // Now that the modal is shown, iterate over the rows
    $('#instructorTableBody tr').each(function(){
        var username = getRowUsername(this);
        var editSelector = "#editButton-" + username;
        var inputSelector = "#inputPhoneNumber-" + username;
        // format the incoming instructor phone number
        $("input[name=courseInstructorPhone]").inputmask('(999)-999-9999');

        if (username){
          setupPhoneNumber(editSelector, inputSelector);
        }
    });
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
  let courseID = action.id;
  let courseAction = action.value;
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
  } else if (courseAction == "Modify"){ 
    showAlterModalWithCourse(courseID);
  } else if(courseAction == "Print"){
    printDocument(`/serviceLearning/print/${courseID}`)
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

/************** Imported Courses Modal Functions **************/
function showAlterModalWithCourse(courseID) {
  getImportedCourseInfo(courseID, function() {
    $('#alterModal #alterCourseId').val(courseID);
    $('#alterModal').modal('show');
  });

  $('#saveButton').on('click', function(event) {
    event.preventDefault();
    var instructorData = getCourseInstructors();
    setInstructorList(instructorData);

    var dynamicRoute = `/manageServiceLearning/imported/${courseID}`;
    var $form = $('#alterModal form');
    $form.attr('action', dynamicRoute);
    $form.submit();
});
}


function getImportedCourseInfo(courseID, callback) { // This function populates the fields in the modal of a chosen course with preexisting data
  $.ajax({
    url: `/manageServiceLearning/imported/${courseID}`,
    type: "GET",
    success: function(courseDict) {
      if (Object.keys(courseDict).length !== 0){
        // update the imported course modal
        $('#courseName').val(courseDict['courseName']);
        $('#courseAbbreviation').val(courseDict['courseAbbreviation']);

        let modalTitle = courseDict['courseName'] ? courseDict['courseName'] : courseDict['courseAbbreviation'] 
        
        // Find the element with class "modal-header" and "fw-bold" using jQuery
        $("#alterModalTitle").text(`Edit ${modalTitle}`);

        $('#hoursEarned').val(courseDict['hoursEarned']);
        if (courseDict['instructors'] && courseDict['instructors'].length > 0) {
          updateInstructorsTable(courseDict['instructors']);
        }
      }
      
      if (callback) callback();
    } 
  });
}

// Instructor manipulation functions

function setInstructorList(instructorData) { // This function attaches the list of usernames to the form submission
  $('#alterModal form input[name="instructor[]"]').remove();
  
  // Append new hidden inputs for each instructor
  for (let i=0; i < instructorData.length; i++) {
      attachInstructorsInfo('#alterModal form', instructorData[i]);
  };
}

function updateInstructorsTable(instructors) { // This function creates row(s) for preexisting instructor(s) in the modal
  // Clear existing table contents except the template row
  $("#instructorTableBody").find("tr:not(:first)").remove();
  $("#instructorTableNames").empty();
  // Add each instructor to the table
  instructors.forEach(function(instructor) {
    var newRow = createInstructorRow(instructor);
    $("#instructorTableBody").append(newRow);
    attachInstructorsInfo('#instructorTableNames', instructor.username);
  });
};

function attachInstructorsInfo(location, value) { // This function regulates attachments of instructors to specific locations in the code (table, form submit, ...)
    $('<input>').attr({
      type: 'hidden',
      name: 'instructor[]',
      value: value
  }).appendTo(location);
}

function createInstructorRow(instructor) {
  // Create a new row element based on the instructor data
  var row = `<tr data-username="${instructor.username}">
                <td>
                  <p class="mb-0">${instructor.firstName} ${instructor.lastName} (${instructor.email})</p>
                  <input type="text" style="border: none" size="14" class="form-control-sm" 
                        id="inputPhoneNumber-${instructor.username}" name="courseInstructorPhone" 
                        aria-label="Instructor Phone" value="${instructor.phoneNumber}" 
                        data-value="${instructor.phoneNumber}" 
                        placeholder="Phone Number" />
                  <a class="text-decoration-none primary editButton" tabindex="0" 
                    data-username="${instructor.username}" id="editButton-${instructor.username}" type="button">Edit</a>
                </td>
                <td class="align-middle">
                  <button id="remove" type="button" class="btn btn-danger removeButton">Remove</button>
                </td>
              </tr>`;
  return row;
}

function emptyInstructorTable() {
  let saveRow = $("#instructorTableBody tr")[0];
  $("#instructorTableBody").empty().html(saveRow);
}

export const allExports = {
  resetAllSelections,
  updateRenewModal,
  changeAction,
  renew,
  withdraw,
  changeTerm,
  formSubmit,
  reviewCourses,
  approveProposal,
  unapproveProposal,
  showAlterModalWithCourse,
  getImportedCourseInfo,
  setInstructorList,
  updateInstructorsTable,
  attachInstructorsInfo,
  createInstructorRow,
  emptyInstructorTable,
}

Object.keys(allExports).forEach(key => {
  window[key] = allExports[key] 
})

window.formSubmit = formSubmit;
window.changeAction = changeAction;
