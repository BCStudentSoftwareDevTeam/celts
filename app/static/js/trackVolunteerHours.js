$(document).ready(function(){

// Search functionalities from the volunteer table in the UI
  $("#trackHoursInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#volunteerTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

// Adding the new volunteer to the user database table
$("#selectVolunteerButton").click(function(){
  user = $("#addVolunteerInput").val()
  volunteerEventID = $("#eventID").val()

  $.ajax({
    url: "/addVolunteerToEvent/" + user+"/"+volunteerEventID,
    type: "POST",
    success: function(message){
      // location.reload();
      msgFlash(message, "success")

    },
    error: function(request, status, error){
      location.reload();
      msgFlash(message, "danger")
      console.log(status,error);
    }

    })
  })
});

// Search functionalities from the user table in the database
function searchTrackHoursVolunteers(){

  $("#selectVolunteerButton").prop('disabled', true)
  var query = $("#addVolunteerInput").val()

  $("#addVolunteerInput").autocomplete({
    appendTo: "#addVolunteerModal",
    minLength: 2,
    source: function(request, response){
      $.ajax({
        url: "/searchTrackHoursVolunteers/" + query,
        type: "GET",
        dataType: "json",
        success: function(dictToJSON) {
          response($.map( dictToJSON, function( item ) {
            return {
            label: item,
            value: dictToJSON[item]
            }
          }))
        },
        error: function(request, status, error) {
          console.log(status,error);
        }
      })
    },
    select: function() {
      $("#selectVolunteerButton").prop('disabled', false)
    }
  });
};



function toggleTrackHoursInputBox(checkbox){
  username =  checkbox.id.substring(9) //get
  console.log(username)
  inputFieldID = 'inputHours_'+username

  if (checkbox.checked){
    console.log($('#'+inputFieldID).val())
    $('#'+inputFieldID).prop('readonly', false)

    eventLength = $("#eventLength").text()
    $('#'+inputFieldID).val(eventLength)

  }else{
    $('#'+inputFieldID).prop('readonly', true)
    $('#'+inputFieldID).val('')
  }


 }
