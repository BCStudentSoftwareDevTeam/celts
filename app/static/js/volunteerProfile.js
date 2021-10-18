$(document).ready(function(){

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

  $(".ban").click(function() {

    $("#banVolunteerButton").text($(this).val() + " Volunteer");
    $(".modal-title").text($(this).val() + " Volunteer");
    $("#modalProgramName").text("Program: " + $(this).attr("name"));
    $("#banVolunteerModal").modal("toggle");
    $("#banVolunteerButton").attr("programID", $(this).attr("id"))
    $("#banVolunteerButton").attr("username", $(".form-check-input").attr("name"))
    $("#banVolunteerButton").attr("banOrUnban", $(this).val());
    $("#ubanEndDate").show()
    $("#banVolunteerEndDate").val("")
    $("#banVolunteerNote").val("")

    if( $(this).val()=="Unban"){
      $("#ubanEndDate").hide()
      $("#banVolunteerEndDate").val("1999-12-31") //This is a placeholder value for the if statement in line 49 to work properly
    }

  });

  $("#banVolunteerNote, #banVolunteerEndDate").change(function () {
    if( ($("#banVolunteerNote").val()) && ($("#banVolunteerEndDate")).val()) {
            $("#banVolunteerButton").prop("disabled", false);
      }
      else {
        $("#banVolunteerButton").prop("disabled", true);
      }

  });

  $("#banVolunteerButton").click(function (){
    console.log("Nothing to see here");

    $.ajax({
      method: "POST",
      url: "/banUnbanUser/" + $(this).attr("programID") + "/" + $(this).attr("username"),
      data: {"note": $("#banVolunteerNote").val(),
             "banOrUnban": $(this).attr("banOrUnban"),
             "endDate":$("#banVolunteerEndDate").val(),
             "username": $(this).attr("username"),
             "programID": $(this).attr("programID")
            },
      success: function(response) {
        console.log("The ban table has been updated", "success");
        location.reload();
      }
    });
  });
});
