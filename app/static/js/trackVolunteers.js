$(document).ready(function(){
  $('[data-bs-toggle="tooltip"]').tooltip();
  $("#trackHoursInput").on("keyup", function() {

// Search functionalities from the volunteer table in the UI
  $("#trackVolunteersInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#volunteerTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});
// Adding the new volunteer to the user database table
$("#selectVolunteerButton").click(function(){
  user = $("#addVolunteerInput").val()
  volunteerEventID = $("#eventID").val()
  eventLengthInHours = $("#eventLength").text()

  $.ajax({
    url: "/addVolunteerToEvent/" + user+"/"+volunteerEventID+"/"+eventLengthInHours,
    type: "POST",
    success: function(s){
      location.reload();

    },
    error: function(request, status, error){
      location.reload();
      console.log(status,error);
    }

  })
})

// Deleting a volunteer from the eventParticipant database table
function removeVolunteerFromEvent (deleteIcon){
  user =  deleteIcon.id.substring(11)
  console.log(user)
  eventID = $('#eventID').val()
  $.ajax({
    url: "/removeVolunteerFromEvent/"+ user +"/"+ eventID,
    type: "POST",
    success: function(s){
      location.reload()

    },
    error: function(request, status, error) {
        console.log(status,error);
    }
  })
}

// Search functionalities from the user table in the database
function searchVolunteers(){

  $("#selectVolunteerButton").prop('disabled', true)
  var query = $("#addVolunteerInput").val()

  $("#addVolunteerInput").autocomplete({
    appendTo: "#addVolunteerModal",
    minLength: 2,
    source: function(request, response){
      $.ajax({
        url: "/searchVolunteers/" + query,
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

function toggleVolunteersInputBox(checkbox){
  username =  checkbox.id.substring(9) //get everything after the 9th character
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
