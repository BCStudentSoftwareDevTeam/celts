// app/static/js/profile.js
import searchUser from './searchUser.js';

function callback(selected) {
  console.log('Selected student:', selected);
  // Set the input value to the full name
  $("#searchStudentsInput").val(`${selected.firstName} ${selected.lastName}`);
  // Set the email field value to the selected student's email
  $("#studentEmail").val(selected.email);
}

$(document).ready(function() {
  $("#searchStudentsInput").on("input", function() {
    console.log("Input event triggered");
    searchUser("searchStudentsInput", callback);
  });

  $("#searchIcon").click(function (e) {
    e.preventDefault();
    console.log("Search icon clicked");
    // Here, you might need to manually get the selected value and set it
    let selected = { firstName: $("#searchStudentsInput").val().split(" ")[0], lastName: $("#searchStudentsInput").val().split(" ")[1] };
    callback(selected);
  });
});

$("input[name='experienceType']").on("change", function() {
  toggleOtherExperienceTextarea();
});

$("input[name='experienceHoursOver300']").on("change", function() {
  toggleTextarea();
});

function toggleTextarea() {
var yesRadio = document.getElementById('yes300hours');
var textareaContainer = document.getElementById('hoursBelow300Container');
if (yesRadio.checked) {
  textareaContainer.style.display = 'none';
} else {
  textareaContainer.style.display = 'block';
}
}

function toggleOtherExperienceTextarea() {
var otherRadio = document.getElementById('otherExperience');
var textareaContainer = document.getElementById('otherExperienceDescription');
if (otherRadio.checked) {
  textareaContainer.style.display = 'block';
} else {
  textareaContainer.style.display = 'none';
}
}