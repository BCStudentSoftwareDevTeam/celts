$(document).ready(function(){

  $(".ban").click(function() {
    $("#banVolunteerButton").text($(this).val() + " Volunteer");
    $("#modalProgramName").text("Program: " + $(this).attr("name"));
    $('#banVolunteerModal').modal('toggle');
  });


  $(".form-check-input").click(function updateInterest(){
    var programID = $(this).attr('id');
    var interest = $(this).is(':checked');
    var username = $(this).attr('name');

    if (interest) {
      var routeUrl = "addInterest";
    }
    else {
      var routeUrl = "deleteInterest";
    }
    interestUrl = "/" + routeUrl + "/" + programID + "/" + username;
    $.ajax({
      method: "POST",
      url: interestUrl,
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
$(".ban").click(function banUnbanUser(){
  $.ajax({
    method: "POST",
    url: "/ban/<program_id>/<username>",
    success: function(response) {
      msgFlash("The ban table has been updated", "success");

    }


  });



});

});
