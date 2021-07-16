$(document).ready(function(){



  $("#trackHoursInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

});

function toggleTrackHoursInputBox(checkbox){
  username =  checkbox.id.substring(9) //get
  console.log(username)
  inputFieldID = 'inputHours_'+username

  if (checkbox.checked){
    console.log($('#'+inputFieldID).val())
    $('#'+inputFieldID).prop('readonly', false)
    console.log($('#startTime').val())

  }else{
    $('#'+inputFieldID).prop('readonly', true)
    $('#'+inputFieldID).val('')
  }


 }
