$(document).ready(function() {
  $('#hoursBelow300Container').hide()
  $('#otherExperienceDescription').hide()

  $('input.phone-input').inputmask('(999)-999-9999')
  $('input.phone-input').on('input', function(){
      let matches = $(this).val().match(/\d/g);
      let digits = matches?matches.length:0;
      if (digits == 0 || digits == 10){
          this.setCustomValidity('')
      }
      else{
          this.setCustomValidity('Please enter a valid phone number.')    
          this.reportValidity()        
      }
  })
  $("input[name='experienceType']").on("change", function() {
    toggleOtherExperienceTextarea();
  });

  $("input[name='experienceHoursOver300']").on("change", function() {
    toggleUnder300HoursTextarea();
  });

  function toggleUnder300HoursTextarea() {
    var yesRadio = $('#yes300hours');
    var conditionalTextBox = $('#hoursBelow300Container');
    if (yesRadio.is(':checked')) {
      conditionalTextBox.hide()
    } else {
      conditionalTextBox.show() 
    }
  }

  function toggleOtherExperienceTextarea() {
    var otherRadio = $('#otherExperience');
    var conditionalTextBox = $('#otherExperienceDescription');
    if (otherRadio.is(':checked')) {
      conditionalTextBox.show()
    } else {
      conditionalTextBox.hide()
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
        location.reload()
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
  });
  $('#otherExperienceForm').on('submit', function(event) {
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
        location.reload()
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
  });
})
