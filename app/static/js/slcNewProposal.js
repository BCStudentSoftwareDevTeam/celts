import searchUser from './searchUser.js'

let currentTab = 0; // Current tab is set to be the first tab (0)

$(document).ready(function(e) {
  $("#cancelButton").hide();
  showTab(currentTab); // Display the current tab
})

function showTab(currentTab) {
  // function that displays the specified tab of the form
  let allTabs = $(".tab");
  $(allTabs[currentTab]).css("display", "block");
  if (currentTab == 0) {
    $("#cancelButton").show();
    $("#previousButton").css("display", "none");
  } else {
    $("#cancelButton").hide();
    $("#previousButton").css("display", "inline");
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

$("#cancelButton").on("click", function() {
  window.location.replace("/serviceLearning/courseManagement");
});

function displayCorrectTab(navigateTab) {
  // This function will figure out which tab to display
  let allTabs = $(".tab");

  if (navigateTab == 1 && !validateForm()) return false;

  $(allTabs[currentTab]).css("display", "none");
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + navigateTab;

  if (currentTab >= allTabs.length) {
    saveCourseInstructors().then(() => $("#slcNewProposal").submit());
    return false;
  }
  showTab(currentTab);
}

function validateForm() {
  // TODO: Generalize form validation to include textareas and selects
  // This function deals with validation of the form fields
  return true;
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
  let data = $("#courseInstructor").val();
  data = data.split(",");
  let instructor = data[0]
  let phone = data[1]
  let tableBody = $("#instructorTable").find("tbody");
  let lastRow = tableBody.find("tr:last");
  let newRow = lastRow.clone();
  newRow.find("td:eq(0) p").text(instructor);
  newRow.find("td:eq(0) div input").val(phone);
  newRow.find("td:eq(0) div button").attr("data-id", instructor);
  newRow.find("td:eq(0) div input").attr("id", instructor);
  newRow.prop("hidden", false);
  lastRow.after(newRow);
}

$("#courseInstructor").on('input', function() {
  searchUser("courseInstructor", callback, null, true);
});

$("#instructorTable").on("click", "#instructorPhoneUpdate", function() {
   var inputId = $(this).attr("data-id")
   console.log($("#" + inputId).val())
   var instructorData = [inputId, $("#" + inputId).val()]

   $.ajax({
     url: "/updateInstructorPhone",
     data: JSON.stringify(instructorData),
     type: "POST",
     contentType: "application/json",
     success: function(response) {
         msgFlash("Instructor's phone number updated", "success")
     },
     error: function(request, status, error) {
       console.log(status,error);
       msgFlash("Error updating phone number", "danger")
     }
   });
});

$("#instructorTable").on("click", "#remove", function() {
   $(this).closest("tr").remove();
});

let courseInstructors = []
async function saveCourseInstructors() {
  $("#instructorTable tr").each(function(a, b) {
    courseInstructors.push($('.instructorName', b).text());
    console.log(courseInstructors)
  });
  return await $.ajax({
    url: "/courseInstructors",
    data: JSON.stringify(courseInstructors),
    type: "POST",
    contentType: "application/json",
    success: function () {}
  });
}
