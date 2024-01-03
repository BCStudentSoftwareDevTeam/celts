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
  } else if (courseAction == "Alter"){ // Beans
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

function saveCourseData(url, successCallback) {
  var formdata = $("form").serialize()
  var instructordata = $.param({"instructor":getCourseInstructors()})
  $.ajax({
      url: url,
      type: "POST",
      data: formdata + "&" + instructordata,
      success: function(response) {
        if (response.redirect) {
          // Redirect to the URL provided by the server
          window.location.href = response.redirect;
      } else {
          // Call the successCallback if you have other logic to handle
          successCallback(response);
      }
  },
      
      error: function(request, status, error) {
       msgFlash("Error saving changes!", "danger")
     }
});
}

function showAlterModalWithCourse(courseID) {
  getImportedCourseInfo(courseID, function() {
    $('#alterModal #alterCourseId').val(courseID);

    // var formAction = `/manageServiceLearning/imported/${courseID}`;

    $("#saveImportedCourses").click(function(){
      $("#saveImportedCourses").prop("disabled", true)
      saveCourseData("/serviceLearning/imported", function(response) {
          window.location.replace("/manageServiceLearning")
      })
  });

    // $('#alterModal form').attr('action', formAction);
    

    $('#alterModal').modal('show');
  });
}


function getImportedCourseInfo(courseID, callback){
  $.ajax({
    url: `/manageServiceLearning/imported/${courseID}`,
    type: "GET",
    success: function(courseDict) {
      console.log(JSON.stringify(courseDict))
      console.log(`Got the course Dict, here it is: ${courseDict}`) // Beans

      if (Object.keys(courseDict).length !== 0){
        // update the alter imported course modal
        $('#courseName').val(courseDict['courseName']);
        $('#courseAbbreviation').val(courseDict['courseAbbreviation']);
        $('#courseCredit').val(courseDict['courseCredit']);

        // Beans: need to update the course instructors. Maybe create a table and add rows to the table in here?
        if (courseDict['instructors'] && courseDict['instructors'].length > 0) {
          updateInstructorsTable(courseDict['instructors']);
        }

      }
      if (callback) callback();
    }
  });
}




function updateInstructorsTable(instructors) {
  // Clear existing table contents except the template row
  $("#instructorTableBody").find("tr:not(:first)").remove();

  // Add each instructor to the table
  instructors.forEach(function(instructor) {
    var newRow = createInstructorRow(instructor);
    $("#instructorTableBody").append(newRow);
  });
}

function createInstructorRow(instructor) {
  // Create a new row element based on the instructor data
  var row = `<tr data-username="${instructor.username}">
               <td>
                 <p class="mb-0">${instructor.firstName} ${instructor.lastName} (${instructor.email})</p>
                 <input type="text" style="border: none" size="14" class="form-control-sm" 
                        name="courseInstructorPhone" aria-label="Instructor Phone" 
                        value="${instructor.phoneNumber}" placeholder="Phone Number" />
                 <a class="text-decoration-none primary editButton" tabindex="0" 
                    data-username="${instructor.username}" type="button">Edit</a>
               </td>
               <td class="align-middle">
                 <button type="button" class="btn btn-danger removeButton">Remove</button>
               </td>
             </tr>`;
  return row;
}


function getCourseInstructors() {
  // get usernames out of the table rows into an array
  return $("#instructorTableNames input").map((i,el) => $(el).val())
}

// function getCourseInstructors() {
//   // Assuming instructors' usernames are stored in data-username attribute of table rows
//   var instructorUsernames = $("#instructorTableBody tr").map(function() {
//       return $(this).data('username');
//   }).get(); // .get() converts the jQuery object to a plain JavaScript array
//   return instructorUsernames;
// }


function changeTerm() {
    $('form').submit();
};

function formSubmit(el) {
    $("#termSelector").attr('action', '/manageServiceLearning/' + el);
    $("#termSelector").submit()
};

function saveCourseData(url, successCallback) {
  console.log("Here you are")
  var formdata = $("form").serialize()
  var instructordata = $.param({"instructor":getCourseInstructors()})
  console.log(formdata + "&" + instructordata)
  $.ajax({
      url: url,
      type: "POST",
      data: formdata + "&" + instructordata,
      success: successCallback,
      error: function(request, status, error) {
       msgFlash("Error saving changes!", "danger")
     }
});
}



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
