$(document).ready(function(){

  $(".form-check-input").click(function updateInterest(){
    var programID = $(this).attr('id');
    var interest = $(this).is(':checked');
    var username = $(this).attr('name');

    var routeUrl = interest ? "addInterest" : "removeInterest";
    interestUrl = "/" + routeUrl + "/" + programID + "/" + username;
    $.ajax({
      method: "POST",
      url: interestUrl,
      success: function(response) {
          msgFlash("Your interest has been updated", "success");
          location.reload(true);  //  Reloading page after user clicks on the show interest checkbox
      },
      error: function(request, status, error) {
        console.log(status,error);
        msgFlash("Error Updating Interest", "danger");
        location.reload(true);
      }
    });
  });

  $(".ban").click(function() {

    $("#banButton").text($(this).val() + " Volunteer");
    $(".modal-title").text($(this).val() + " Volunteer");
    $("#modalProgramName").text("Program: " + $(this).attr("name"));
    $("#banModal").modal("toggle");
    $("#banButton").attr("programID", $(this).attr("id"))
    $("#banButton").attr("username", $(".form-check-input").attr("name"))
    $("#banButton").attr("banOrUnban", $(this).val());
    $("#ubanEndDate").show()
    $("#banNoteDiv").hide()
    $("#banEndDate").val("")
    $("#banVolunteerNote").val("")

    if( $(this).val()=="Unban"){
      $("#ubanEndDate").hide()
      $("#banEndDate").val("0001-01-01") //This is a placeholder value for the if statement in line 49 to work properly
      $("#banNoteDiv").show()
      $("#banNote").text($(this).attr("note"))
    }

  });

  $("#banVolunteerNote, #banEndDate").change(function () {
    var enableButton = ($("#banVolunteerNote").val() && $("#banEndDate").val());
    $("#banButton").prop("disabled", !enableButton);
  });

  $("#banButton").click(function (){
    $.ajax({
      method: "POST",
      url: "/" + ($(this).attr("banOrUnban")).toLowerCase() + "User/" + $(this).attr("programID") + "/" + $(this).attr("username"),
      data: {"note": $("#banVolunteerNote").val(),
             "endDate":$("#banEndDate").val()
            },
      success: function(response) {
        location.reload();
      }
    });
  });
});
