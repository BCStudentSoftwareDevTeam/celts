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
    $("#approveButton").show();
    $("#nextButton").text("Submit");
  } else {
    $("#approveButton").hide();
    $("#nextButton").text("Next");
  }
  fixStepIndicator(currentTab)
}

$("#approveButton").click(function(){
  var data = $("form").serialize()
  saveCourseInstructors()
  $.ajax({
    url: "/serviceLearning/approveCourse/",
    type: "POST",
    data: data,
    success: function(response) {
        window.location.replace("/manageServiceLearning")
        msgFlash("Course approved!", "success")
    }
  });
});

$("#previousButton").on("click", function() {
  displayCorrectTab(-1);
});

$("#nextButton").on("click", function() {
  displayCorrectTab(1);
});

$("#cancelButton").on("click", function() {
  window.location.replace("/manageServiceLearning");
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
  let valid = true;
  let allTabs = $(".tab");
  let allInputs = $(allTabs[currentTab]).find("input");
  for (let i = 0; i < allInputs.length; i++) {
    if (allInputs[i].required) {
      if (!allInputs[i].value){
        allInputs[i].className += " invalid";
        valid = false;
      } else {
        allInputs[i].className = "form-control";
      }
    }
  }

  if ($("table").find('td').length < 5 && currentTab ==1) { // checks if there are more than the default hidden 3 tds
    valid = false;
    $("#courseInstructor").addClass("invalid");
  } else {
    $("#courseInstructor").removeClass("invalid");
  }
  if (valid) {
    $(".step")[currentTab].className += " finish";
  }
  return valid;
};

function fixStepIndicator(navigateTab) {
  // This function updates the active step indicator
  let steps = $(".step");
  for (let i = 0; i < steps.length; i++) {
    steps[i].className = steps[i].className.replace(" active", "");
  }
  steps[navigateTab].className += " active";
}

function callback() {
  // JSON.parse is required to de-stringify the search results into a dictionary.
  let data = JSON.parse($("#courseInstructor").val());
  let instructor = (data["firstName"]+" "+data["lastName"]+" ("+data["username"]+")");
  let username = data["username"];
  let phone = data["phoneNumber"];
  let tableBody = $("#instructorTable").find("tbody");
  let lastRow = tableBody.find("tr:last");
  let newRow = lastRow.clone();
  newRow.find("td:eq(0) p").text(instructor);
  newRow.find("td:eq(0) div input").val(phone);
  newRow.find("td:eq(0) div button").attr("data-id", username);
  newRow.find("td:eq(0) div input").attr("id", username);
  newRow.prop("hidden", false);
  lastRow.after(newRow);
}

$("#courseInstructor").on('input', function() {
  // To retrieve specific columns into a dict, create a [] list and put columns inside
  searchUser("courseInstructor", callback, true, null, ["phoneNumber", "firstName", "lastName", "username"]);
});

$("#instructorTable").on("click", "#instructorPhoneUpdate", function() {
   var inputId = $(this).attr("data-id")
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
  });
  return await $.ajax({
    url: "/courseInstructors",
    data: JSON.stringify(courseInstructors),
    type: "POST",
    contentType: "application/json",
    success: function () {}
  });
}
