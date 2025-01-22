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
})
