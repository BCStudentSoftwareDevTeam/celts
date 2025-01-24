$(document).ready(function() {
  $('#hoursBelow300Container').hide()
  $('#otherExperienceDescription').hide()

  $("input[name='experienceType']").on("change", function() {
    toggleOtherExperienceTextarea();
  });

  $("input[name='experienceHoursOver300']").on("change", function() {
    toggleUnder300HoursTextarea();
  });

  function toggleUnder300HoursTextarea() {
    var yesRadio = $('#yes300hours');
    var textareaContainer = $('#hoursBelow300Container');
    if (!yesRadio.checked) {
      textareaContainer.show()
    }
  }

  function toggleOtherExperienceTextarea() {
    var otherRadio = $('#otherExperience');
    var textareaContainer = $('#otherExperienceDescription');
    if (otherRadio.checked) {
      textareaContainer.style.display = 'block';
    } else {
      textareaContainer.style.display = 'none';
    }
  }

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
})
