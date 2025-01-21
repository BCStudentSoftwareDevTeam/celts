import searchUser from './searchUser.js';

function callback(selected) {
  $("#searchStudentsInput").val(`${selected.firstName} ${selected.lastName}`);
  $("#studentEmail").val(selected.email);
}

$(document).ready(function() {
  $("#searchStudentsInput").on("input", function() {
    searchUser("searchStudentsInput", callback);
  });

  $("#searchIcon").click(function (e) {
    e.preventDefault();
    let selected = { firstName: $("#searchStudentsInput").val().split(" ")[0], lastName: $("#searchStudentsInput").val().split(" ")[1] };
    callback(selected);
  });

  $("input[name='experienceType']").on("change", function() {
    toggleOtherExperienceTextarea();
  });

  $("input[name='experienceHoursOver300']").on("change", function() {
    toggleTextarea();
  });

  function toggleTextarea() {
    var yesRadio = $('#yes300hours');
    var textareaContainer = $('#hoursBelow300Container');
    if (yesRadio.checked) {
      textareaContainer.style.display = 'none';
    } else {
      textareaContainer.style.display = 'block';
    }
  }
  window.toggleTextarea = toggleTextarea; 

  function toggleOtherExperienceTextarea() {
    var otherRadio = $('#otherExperience');
    var textareaContainer = $('#otherExperienceDescription');
    if (otherRadio.checked) {
      textareaContainer.style.display = 'block';
    } else {
      textareaContainer.style.display = 'none';
    }
  }
  window.toggleOtherExperienceTextarea = toggleOtherExperienceTextarea;

  function updateYearOptions() {
    var submissionDate = new Date($('#date').value);
    var currentYear = submissionDate.getFullYear();
    var month = submissionDate.getMonth() + 1;
    var day = submissionDate.getDate();
    var defaultYear = (month < 5 || (month === 5 && day < 16)) ? currentYear : currentYear + 1;

    var startYear = currentYear - 3;
    var endYear = currentYear + 2;

    var options = [];
    for (var year = startYear; year <= endYear; year++) {
      var option = $("<option>").val(year).text(year);
      if (year === defaultYear) {
        option.attr("selected", "selected");
      }
      options.push(option);
    }

    $("#summerYear").empty().append(options);
  }

  var today = new Date().toISOString().split('T')[0];
  $('#date').value = today;
  updateYearOptions();

  $('#date').addEventListener('change', updateYearOptions);

  $('#summerExperienceForm').on('submit', function(event) {
    event.preventDefault(); 
    var formData = new FormData(this); 
    var actionUrl = $(this).attr('action'); 
    
    $.ajax({
      url: actionUrl,
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function(response) {
        $('#pills-training').html(response);
        $('#trainingEvents').tab('show');
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
  });
 $('#edit-proposal-button').on('click', function() {
    toggleEditMode(true);
  });

  $('#cancel-edit-button').on('click', function() {
    toggleEditMode(false);
  });

  function toggleEditMode(isEditMode) {
    document.querySelectorAll('input, textarea, select').forEach(element => {
      if (element.type === 'radio' || element.type === 'checkbox' || element.tagName === 'SELECT') {
        element.disabled = !isEditMode;
      } else {
        element.readOnly = !isEditMode;
      }
    });
    $('#edit-buttons').style.display = isEditMode ? 'block' : 'none';
    $('#view-buttons').style.display = isEditMode ? 'none' : 'block';
  }

  toggleEditMode(false);


// ////////// js for Requesting Other Engagement //////////
document.addEventListener('DOMContentLoaded', function() {
  // Function to get query parameters
  function getQueryParams() {
      let params = {};
      window.location.search.substring(1).split("&").forEach(function(pair) {
          let [key, value] = pair.split("=");
          params[key] = value;
      });
      return params;
  }

  // Set the active tab based on the query parameter
  const params = getQueryParams();
  if (params.tab === 'otherEngagement') {
      const otherEngagementTab = $('#otherEngagementTab'); // Adjust this to your tab element's ID
      const tabContent = $('#otherEngagement'); // Adjust this to your tab content's ID
      otherEngagementTab.classList.add('active');
      tabContent.classList.add('active', 'show');
  }

  // Fetch terms and populate the select dropdown
  fetch('/api/terms')
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok ' + response.statusText);
          }
          return response.json();
      })
      .then(data => {
          const termSelect = $('#inputTerm');
          const termId = document.querySelector('form').dataset.termId;
          data.forEach(term => {
              const option = document.createElement('option');
              option.value = term.id;
              option.textContent = term.name;  // Using 'name' which is actually 'description' in the model
              termSelect.appendChild(option);
              if (term.id == termId) {
                  option.selected = true;
              }
          });
      })
      .catch(error => console.error('Error fetching terms:', error));

  const editOtherButton = $('#edit-other-proposal-button');
  const cancelOtherButton = $('#cancel-other-edit-button');
  const otherFormFields = $('#requestOtherCommEng input, #requestOtherCommEng select, #requestOtherCommEng textarea');

  editOtherButton.addEventListener('click', function() {
      otherFormFields.forEach(field => field.removeAttribute('disabled'));
      $('#edit-other-buttons').style.display = 'block';
      $('#view-other-buttons').style.display = 'none';
  });

  cancelOtherButton.addEventListener('click', function() {
      otherFormFields.forEach(field => field.setAttribute('disabled', 'disabled'));
      $('#edit-other-buttons').style.display = 'none';
      $('#view-other-buttons').style.display = 'block';
  });
