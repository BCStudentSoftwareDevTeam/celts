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
      window.location.replace($(this).val());
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
  // -----------------------------------------
      $("#instructorTable").on("click", "#remove", function() {
        let closestRow =  $(this).closest("tr")
        $("#instructorTableNames input[value="+closestRow.data('username')+"]").remove()
        closestRow.remove();
      });
      $("#courseInstructor").on('input', function() {
          searchUser("courseInstructor", createNewRow, true, null, "instructor");
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
    $("#submitAndApproveButton").hide();
    $(".editButton").hide()
    $(".removeButton").hide()
    $(".slcQuestionWordCounter").replaceWith(" ");
}



function readOnly() {
    return window.location.href.includes("view");
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
        $("#cancelButton").show();
        $("#previousButton").hide();
        $("#submitAndApproveButton").hide();
        $("#nextButton").text("Next");
        $("#nextButton").show();
        $("#saveContinue").hide();
        $("#saveExit").hide()
        $("#exitButton").hide()
        break;
    case 1: // Second page
        $("#cancelButton").hide();
        $("#previousButton").show();
        $("#submitAndApproveButton").hide();
        $("#nextButton").hide();
        $("#saveContinue").show();
        $("#saveContinue").text("Next");
        $("#saveExit").show()
        $("#exitButton").hide()
        if(readOnly()) {
            $("#nextButton").show();
            $("#saveContinue").hide();
            $("#saveExit").hide()
            $(".removeAttachment").hide()
            $("#exitButton").hide()
        }
        break;
    case 2: // Third page
        $("#cancelButton").hide();
        $("#previousButton").show();
        $("#submitAndApproveButton").show();
        $("#nextButton").text("Submit Proposal");
        $("#nextButton").show();
        $("#saveContinue").hide();
        $("#exitButton").hide()
        if(readOnly()) {
            $("#nextButton").text("Next");
            $("#nextButton").hide();
            $("#submitAndApproveButton").hide();
            $("#exitButton").show()
          }
        break;
    }

  fixStepIndicator(currentTab)
}

// Form Submission Functions
// --------------------------------------------------

function saveCourseData(url, successCallback) {
    if (!validateForm()) return false;

    var formdata = $("form").serialize()
    var instructordata = $.param({"instructor":getCourseInstructors()})
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

function validateForm() {
  // This function ensures our form fields are valid
  // Returns true if we are just viewing a form
  // TODO: Generalize form validation to include textareas and selects

  if (readOnly())
      return true;

  let valid = true;

  let allTabs = $(".tab");
  let allInputs = $(allTabs[currentTab]).find("input");
  for (let i = 0; i < allInputs.length; i++) {
    if (allInputs[i].required) {
      if (!allInputs[i].value){
        $(allInputs[i]).addClass("invalid");
        valid = false;
      } else {
        $(allInputs[i]).addClass("form-control");
      }
    }
  }
  var instructors = getCourseInstructors()
  if (!instructors.length && currentTab == 1) {
    valid = false;
    $("#courseInstructor").addClass("invalid");
  } else {
    $("#courseInstructor").removeClass("invalid");
  }

  if (valid) {
    $($(".step")[currentTab]).addClass("finish");
  }

  return valid;
};

// Instructor manipulation functions
// -------------------------------------
//

function getRowUsername(element) {
    return $(element).closest("tr").data("username")
}

function createNewRow(selectedInstructor) {
  let instructor = (selectedInstructor["firstName"]+" "+selectedInstructor["lastName"]+" ("+selectedInstructor["email"]+")");
  let username = selectedInstructor["username"];
  let phone = selectedInstructor["phoneNumber"];
  let tableBody = $("#instructorTable").find("tbody");
  if(tableBody.prop('outerHTML').includes(instructor)){
    msgFlash("Instructor is already added.", "danger");
    return;
  }
  // Create new table row and update necessary attributes
  let lastRow = tableBody.find("tr:last");
  let newRow = lastRow.clone();

  let instructorName = newRow.find("td:eq(0) p")
  instructorName.text(instructor);

  let phoneInput = newRow.find("td:eq(0) input")
  phoneInput.val(phone);
  phoneInput.attr("id", "inputPhoneNumber-" +username);
  $(phoneInput).inputmask('(999)-999-9999');

  let removeButton = newRow.find("td:eq(1) button")
  let editLink = newRow.find("td:eq(0) a")
  editLink.attr("id", "editButton-" + username);

  editLink.attr("data-username", username)
  newRow.prop("hidden", false);
  lastRow.after(newRow);

  phoneInput.attr("data-value", phone)
  var edit = "#editButton-" + username
  var input = "#inputPhoneNumber-" + username
  if (username){
    setupPhoneNumber(edit, input)
  }

  $("#instructorTableNames").append('<input hidden name="instructor[]" value="' + username + '"/>')
}

function getCourseInstructors() {
  // get usernames out of the table rows into an array
  return $("#instructorTableNames input").map((i,el) => $(el).val())
}

function disableSyllabusUploadFile() {
  $("#fileUpload").prop("disabled", true);
}

function enableSyllabusUploadFile() {
    $("#fileUpload").prop("disabled", false);
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



