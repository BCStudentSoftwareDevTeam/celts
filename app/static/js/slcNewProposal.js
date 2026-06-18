import {getCourseInstructors, getRowUsername, createNewRow, updateEmptyTableMessage} from './instructorTable.js'
import searchUser from './searchUser.js'

var currentTab = 0; // Current tab is set to be the first tab (0)

$(document).ready(function(e) {
  handleFileSelection("attachmentObject")

  // set up the current tab and button state
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('tab')){
    currentTab = Number(urlParams.get('tab'));
  }

  showTab(currentTab);

  // Update display if we are viewing only
  if (readOnly()){
      disableInput()
  }

  // set up phone numbers
  $("input[name=courseInstructorPhone]").inputmask('(999)-999-9999');

  // Add button event handlers
  // -----------------------------------------
  $("a.guidelines").on("click", function() {
      let allTabs = $(".tab");
      if (currentTab == (allTabs.length - 2)) {
        displayCorrectTab(-1);
      }
      else if (currentTab == (allTabs.length - 1)){
        displayCorrectTab(-2);
      }
      return false;
  });
  // one-time check to set the initial state
  if ($("#allSectionsSL").is(":checked")) {
    $("#slDesignationGroup").hide();
  }
  $("#allSectionsSL").on("click", function() {
    if ($("#allSectionsSL").is(":checked")) {
      $("#slDesignationGroup").hide();
    }
    else {
      $("#slDesignationGroup").show();
    }
  })
  if ($("#noSlcComponent").is(":checked")) {
    $("#permanentDesignationGroup").hide();
  }
  $("#slcComponent").on("click", function() {
    if ($("#noSlcComponent").is(":checked")) {
      $("#permanentDesignationGroup").hide();
    }
    else {
      $("#permanentDesignationGroup").show();
    }
  })
  if ($("#notPreviouslyApproved").is(":checked")) {
    $("#previouslyApprovedProposal").hide();
  }
  $("#previouslyApprovedGroup").on("click", function() {
    if ($("#notPreviouslyApproved").is(":checked")) {
      $("#previouslyApprovedProposal").hide();
    }
    else {
      $("#previouslyApprovedProposal").show();
    }
  })

  $("#previousButton").on("click", function() {
      displayCorrectTab(-1);
  });

  $("#nextButton").on("click", function() {
      displayCorrectTab(1);
  });

  $("#cancelButton").on("click", function() {
    var cancelButton = $(this)
      $.ajax({
        url: '/serviceLearning/canceledProposal',
        method: 'POST',
        data: {courseID : document.getElementById('courseID').value},
        success: function(response) {
            window.location.replace(cancelButton.val());
        }
      })
  });

  $("#saveContinue").on("click", function() {
      if(readOnly()) {
          let allTabs = $(".tab");
          displayCorrectTab(1)
          if (currentTab == (allTabs.length - 2)) {
            displayCorrectTab(1);
          }
          else if (currentTab == (allTabs.length - 1)){
              // TODO nothing?
          }
      }
      else{
        if (!validateForm()) return;
        $('#slcNewProposal').attr("action", "/serviceLearning/saveProposal")
        $('#slcNewProposal').submit()
      }
  });

  $('#saveExit').on("click", function(){
    if (!validateForm()) return;
    $('#slcNewProposal').attr("action", "/serviceLearning/saveExit")
    $('#slcNewProposal').submit()
  })

  $("#exitButton").on("click", function() {
    window.location.replace('/serviceLearning/exit')
  })

  if(!readOnly()) {
      $("#submitAndApproveButton").click(function(){
          $("#submitAndApproveButton").prop("disabled", true)
          saveCourseData("/serviceLearning/approveCourse", function(response) {
              window.location.replace("/manageServiceLearning")
          })
      });

  // Add course instructor event handlers
  $("#instructorTable").on("click", ".removeButton", function() {  
    let closestRow = $(this).closest("tr");
    let username = closestRow.data('username');
    
    // Check if the username is not empty or undefined
    if (username) {
        $("#instructorTableNames input[value='" + username + "']").remove();
        closestRow.remove();
         msgFlash(`Successfully removed instructor ${username}`, "success", 1300);
    }
    updateEmptyTableMessage();
  });

  $("#courseInstructor").on("focusout", function(){
    $("#courseInstructor").val("")
  })

  $("#courseInstructor").on('input', function() {
      searchUser("courseInstructor", createNewRow, true, null, "instructor");
  });

  $("#courseInstructor").popover({
    trigger: "hover",
    sanitize: false,
    html: true,
    content: function() {
        return $(this).data('tooltip');
    }
  });

    // for each row in instructorTable that has an instructor, pass that instructors phone data to setupPhoneNumber
    $('#instructorTable tr').each(function(){
      var username = getRowUsername(this)
      var edit = "#editButton-" + username
      var input = "#inputPhoneNumber-" + username
      if (username){
        setupPhoneNumber(edit, input)
      }
    })
  }
})

// display functions
// --------------------------------

function disableInput() {
    $("input").prop("disabled", true);
    $("select").prop("disabled", true);
    $("textarea").prop("disabled", true);
    $("#slcQuestionOne").replaceWith( "<ul>" + $( "#slcQuestionOne" ).text() + "</ul>" );
    $("#slcQuestionTwo").replaceWith( "<ul>" + $( "#slcQuestionTwo" ).text() + "</ul>" );
    $("#slcQuestionThree").replaceWith( "<ul>" + $( "#slcQuestionThree" ).text() + "</ul>" );
    $("#slcQuestionFour").replaceWith( "<ul>" + $( "#slcQuestionFour" ).text() + "</ul>" );
    $("#slcQuestionFive").replaceWith( "<ul>" + $( "#slcQuestionFive" ).text() + "</ul>" );
    $("#slcQuestionSix").replaceWith( "<ul>" + $( "#slcQuestionSix" ).text() + "</ul>" );
    $(".view").prop("disabled", true);
    $("#syllabusUploadButton").prop("disabled", true);
    hideButton("#submitAndApproveButton");
    $(".editButton").hide()
    $(".removeButton").hide()
    $(".slcQuestionWordCounter").replaceWith(" ");
}



function readOnly() {
    return window.location.href.includes("view");
}

function showButton(buttonSelector) {
    let button = $(buttonSelector);
    button.show();
    button.closest(".proposal-button-wrapper").show();
}

function hideButton(buttonSelector) {
    let button = $(buttonSelector);
    button.hide();
    button.closest(".proposal-button-wrapper").hide();
}

function fixStepIndicator(navigateTab) {
  // This function updates the active step indicator
  let steps = $(".step");
  steps.each((i, step) => $(step).removeClass("active"));
  $(steps[navigateTab]).addClass("active")
}

function displayCorrectTab(navigateTab) {
  // This function will figure out which tab to display
  let allTabs = $(".tab");
  if (navigateTab == 1 && !validateForm()) return false;

  // hide the current display
  if(currentTab != (allTabs.length - 1) || (navigateTab < 0)){
      $(allTabs[currentTab]).css("display", "none");
  }

  // Increase or decrease the current tab:
  currentTab = currentTab + navigateTab;

  if (currentTab >= allTabs.length) {
      $("#nextButton").prop("disabled", true)
      $("#slcNewProposal").submit();
      return false;
  }
  showTab(currentTab);
}

function showTab(currentTab) {
  // function that displays the specified tab of the form
  let allTabs = $(".tab");
  $(allTabs[currentTab]).css("display", "block");

  switch(currentTab) {
    case 0: // First page
        showButton("#cancelButton");
        hideButton("#previousButton");
        hideButton("#submitAndApproveButton");
        $("#nextButton").text("Next");
        showButton("#nextButton");
        hideButton("#saveContinue");
        hideButton("#exitButton")
        showButton("#saveExit");
        if(readOnly()) {
            hideButton("#saveExit");
            showButton("#exitButton")
        }
        break;
    case 1: // Second page
        hideButton("#cancelButton");
        showButton("#previousButton");
        hideButton("#submitAndApproveButton");
        hideButton("#nextButton");
        showButton("#saveContinue");
        $("#saveContinue").text("Next");
        showButton("#saveExit")
        hideButton("#exitButton")
        if(readOnly()) {
            showButton("#nextButton");
            hideButton("#saveContinue");
            hideButton("#saveExit")
            $(".removeAttachment").hide()
            showButton("#exitButton")
        }
        break;
    case 2: // Third page
        hideButton("#cancelButton");
        showButton("#previousButton");
        showButton("#submitAndApproveButton");
        $("#nextButton").text("Submit Proposal");
        showButton("#nextButton");
        hideButton("#saveContinue");
        hideButton("#exitButton")
        showButton("#saveExit")
        if(readOnly()) {
            $("#nextButton").text("Next");
            hideButton("#nextButton");
            hideButton("#saveExit");
            hideButton("#submitAndApproveButton");
            showButton("#exitButton")
          }
        break;
    }

  fixStepIndicator(currentTab)
}

// Form Submission Functions
// --------------------------------------------------

function saveCourseData(url, successCallback) {
    if (!validateForm()) return false;
    var formData = $("form").serialize()
    var instructorData = $.param(getCourseInstructors())

    $.ajax({
        url: url,
        type: "POST",
        data: formData + "&" + instructorData,
        success: successCallback,
        error: function(request, status, error) {
         msgFlash("Error saving changes!", "danger")
       }
  });
}

function validateForm() {
  // This function ensures our form fields are valid
 enableLiveCustomValidityClearing(["#courseInstructor", "#courseNameId"]);
  if (readOnly())
    return true;

  let valid = true;
  let allTabs = $(".tab");

  //Validating the instructor dropdown
  if (currentTab === 1) {
      let $courseInstructor = $("#courseInstructor");
      let instructorRows = $("tr[data-username]");
      
  if (instructorRows.length === 1) {
      $courseInstructor[0].setCustomValidity("Please select an instructor");
      // Focus and show validation immediately
      $courseInstructor.focus();
      $courseInstructor[0].reportValidity();
      valid = false;
      return valid; // Exit early to prevent other validations from interfering
    }
}

  // Course name validation
  if (currentTab === 1) {
    let $courseName = $("#courseNameId");
    if ($courseName.val() === "") {
      $courseName[0].setCustomValidity("Please enter a course");
      $courseName.focus();
      $courseName[0].reportValidity();
      valid = false;
      return valid; // Exit early
    }
  }

  return valid;
};


function disableSyllabusUploadFile() {
  $("#fileUpload").prop("disabled", true);
}

const textareas = $(".textarea");
const slcQuestionWordCount = $(".slcQuestionWordCounter span")

function calculateCountWords(text){
  const words = text.split(/\s+/);
  return words.length - 1;
}

textareas.each(function(index, textarea){
  $(textarea).on("input", function(){
    const wordCount = calculateCountWords($(textarea).val());
    $(slcQuestionWordCount[index]).html(wordCount);

  });
  const initialWordCount = calculateCountWords($(textarea).val());
  $(slcQuestionWordCount[index]).html(initialWordCount);
});
