import searchUser from './searchUser.js'

let currentTab = 0; // Current tab is set to be the first tab (0)

$(document).ready(function(e) {
  showTab(currentTab); // Display the current tab
})

function showTab(currentTab) {
  // function that displays the specified tab of the form
  let allTabs = $(".tab");
  $(allTabs[currentTab]).css("display", "block");
  if (currentTab == 0) {
    // TODO: make sure cancel redirects to management page. 
    $("#previousButton").text("Cancel");
  } else {
    $("#previousButton").text("Previous");
  }

  if (currentTab == (allTabs.length - 1)) {
    $("#nextButton").text("Submit");
  } else {
    $("#nextButton").text("Next");
  }
  fixStepIndicator(currentTab)
}

$("#previousButton").on("click", function() {
  displayCorrectTab(-1);
});

$("#nextButton").on("click", function() {
  displayCorrectTab(1);
});

function displayCorrectTab(navigateTab) {
  // This function will figure out which tab to display
  let allTabs = $(".tab");

  if (navigateTab == 1 && !validateForm()) return false;
  $(allTabs[currentTab]).css("display", "none");
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + navigateTab;

  if (currentTab >= allTabs.length) {
    saveCourseInstructors().then($("#slcNewProposal").submit());
    return false;
  }
  showTab(currentTab);
}

function validateForm() {
  // TODO: Generalize form validation to include textareas and selects
  // This function deals with validation of the form fields
  let valid = true;
  let allTabs = $(".tab");
  let allInputs = $(allTabs[currentTab]).find("input");

  for (let i = 0; i < allInputs.length; i++) {
    if (allInputs[i].value == "") {
      allInputs[i].className += " invalid";
      valid = false;
    }
  }
  if (valid) {
    $(".step")[currentTab].className += " finish"
  }
  return valid;
}

function fixStepIndicator(navigateTab) {
  // This function updates the active step indicator
  let steps = $(".step");
  for (let i = 0; i < steps.length; i++) {
    steps[i].className = steps[i].className.replace(" active", "");
  }
  steps[navigateTab].className += " active";
}

// TODO: empty the courseInstructor input after an instructor has been added to the table.
function callback() {
  let instructor = $("#courseInstructor").val();
  let tableBody = $("#instructorTable").find("tbody");
  let lastRow = tableBody.find("tr:last");
  let newRow = lastRow.clone();
  newRow.find("td:eq(0)").text(instructor);
  newRow.prop("hidden", false);
  lastRow.after(newRow);
}

$("#courseInstructor").on('input', function() {
  searchUser("courseInstructor", callback);
});

$("#instructorTable").on("click", "#remove", function() {
   $(this).closest("tr").remove();
});

let courseInstructors = []
function saveCourseInstructors() {
  $("#instructorTable tr").each(function(a, b) {
    courseInstructors.push($('.instructorName', b).text());
  });
  return $.ajax({
    url: "/courseInstructors",
    data: JSON.stringify(courseInstructors),
    type: "POST",
    contentType: "application/json",
    success: function () {
      console.log("success");
    }
  });
}
