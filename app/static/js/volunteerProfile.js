$(document).ready(function(){

  $(".ban").click(function() {
    $("#banVolunteerButton").text($(this).val() + " Volunteer");
    $("#modalProgName").text("Program: " + $(this).closest("tr").children("td.programName").text());
    $('#banVolunteerModal').modal('toggle');
  });


  $(".form-check-input").click(function updateInterest(){
    var programID = $(this).attr('id');
    var interest = $(this).is(':checked'); //.prop('checked', true);
    var username = $(this).attr('name');
    console.log(username);
    // var volunteer = $()
    // console.log("+", programID,"-", interest,"=",volunteer);

    if (interest) {
      var routeUrl = "addInterest";
      // rule = true;
    }
    else {
      var routeUrl = "deleteInterest";
      // rule = false;
    }

    $.ajax({
      method: "POST",
      url: "/" + routeUrl + "/" + programID + "/" + username,
      // data: {volunteer: volunteer, programID: programID, rule:rule},
      success: function(response) {
          msgFlash("Your interest has been updated", "success");
      },
      error: function(request, status, error) {
        console.log(status,error);
        msgFlash("Error Updating Interest", "danger");
        window.location.reload(true);
      }
    });
  });


});
