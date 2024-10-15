import searchUser from './searchUser.js';

function callback(selected) {
  console.log('Selected student:', selected);
  $("#searchStudentsInput").val(`${selected.firstName} ${selected.lastName}`);
  $("#studentEmail").val(selected.email);
}

$(document).ready(function() {
  $("#searchStudentsInput").on("input", function() {
    console.log("Input event triggered");
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
    var yesRadio = document.getElementById('yes300hours');
    var textareaContainer = document.getElementById('hoursBelow300Container');
    if (yesRadio.checked) {
      textareaContainer.style.display = 'none';
    } else {
      textareaContainer.style.display = 'block';
    }
  }
  window.toggleTextarea = toggleTextarea; 

  function toggleOtherExperienceTextarea() {
    var otherRadio = document.getElementById('otherExperience');
    var textareaContainer = document.getElementById('otherExperienceDescription');
    if (otherRadio.checked) {
      textareaContainer.style.display = 'block';
    } else {
      textareaContainer.style.display = 'none';
    }
  }
  window.toggleOtherExperienceTextarea = toggleOtherExperienceTextarea;

  function updateYearOptions() {
    var submissionDate = new Date(document.getElementById('date').value);
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
  document.getElementById('date').value = today;
  updateYearOptions();

  document.getElementById('date').addEventListener('change', updateYearOptions);

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

  document.getElementById('edit-proposal-button').addEventListener('click', function() {
    toggleEditMode(true);
  });

  document.getElementById('cancel-edit-button').addEventListener('click', function() {
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
    document.getElementById('edit-buttons').style.display = isEditMode ? 'block' : 'none';
    document.getElementById('view-buttons').style.display = isEditMode ? 'none' : 'block';
  }

  toggleEditMode(false);

  var withdrawButton = document.getElementById('withdraw-button');
  var experienceIdElement = document.getElementById('experience-id');

  if (withdrawButton && experienceIdElement) {
    var experienceId = experienceIdElement.value;

    withdrawButton.addEventListener('click', function(event) {
      event.preventDefault();

      if (confirm('Are you sure you want to withdraw the proposal?')) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', `/profile/${document.getElementById('username').value}/withdrawSummerExperience`, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        xhr.onload = function() {
          if (xhr.status === 200) {
            console.log('Proposal withdrawn successfully');
            window.location.href = `/cceMinor/${document.getElementById('username').value}/viewProposal`;
          } else {
            console.log('Error withdrawing proposal');
          }
        };

        xhr.onerror = function() {
          console.log('Request failed');
        };

        xhr.send('experience_id=' + encodeURIComponent(experienceId));
      } else {
        console.log('User cancelled withdrawal');
      }
    });
  } else {
    console.log('Withdraw button or experience ID not found');
  }
});



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
      const otherEngagementTab = document.getElementById('otherEngagementTab'); // Adjust this to your tab element's ID
      const tabContent = document.getElementById('otherEngagement'); // Adjust this to your tab content's ID
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
          const termSelect = document.getElementById('inputTerm');
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

  const editOtherButton = document.getElementById('edit-other-proposal-button');
  const cancelOtherButton = document.getElementById('cancel-other-edit-button');
  const withdrawOtherButton = document.getElementById('withdraw-other-button');
  const otherFormFields = document.querySelectorAll('#requestOtherCommEng input, #requestOtherCommEng select, #requestOtherCommEng textarea');

  editOtherButton.addEventListener('click', function() {
      otherFormFields.forEach(field => field.removeAttribute('disabled'));
      document.getElementById('edit-other-buttons').style.display = 'block';
      document.getElementById('view-other-buttons').style.display = 'none';
  });

  cancelOtherButton.addEventListener('click', function() {
      otherFormFields.forEach(field => field.setAttribute('disabled', 'disabled'));
      document.getElementById('edit-other-buttons').style.display = 'none';
      document.getElementById('view-other-buttons').style.display = 'block';
  });

  withdrawOtherButton.addEventListener('click', function() {
      const experienceId = document.getElementById('other-experience-id').value;
      if (experienceId && confirm('Are you sure you want to withdraw this proposal?')) {
          fetch(`/withdrawOtherExperience/${experienceId}?tab=otherEngagement`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ experienceId: experienceId })
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  alert('Proposal withdrawn successfully.');
                  window.location.search = "?tab=otherEngagement"; // Update URL to keep the tab
              } else {
                  alert('Failed to withdraw the proposal.');
              }
          })
          .catch(error => console.error('Error withdrawing proposal:', error));
      }
  });
});