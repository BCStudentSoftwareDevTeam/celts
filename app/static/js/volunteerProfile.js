$(document).ready(function(){
  $(".form-check-input").click(function updateInterest(){
    var programID = $(this).data("programid");
    var username = $(this).data('username');

    var interest = $(this).is(':checked');
    var routeUrl = interest ? "addInterest" : "removeInterest";
    interestUrl = "/" + username + "/" + routeUrl + "/" + programID ;

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

  // This function is to disable all the dates before current date in the ban modal End Date picker
  $(function(){
    var banEndDatepicker = $("#banEndDatepicker");
    banEndDatepicker.datepicker({
      changeYear: true,
      changeMonth: true,
      minDate:+1,
      dateFormat: "yy-mm-dd",
    }).attr('readonly','readonly');
  });



  $(".ban").click(function() {
    var banButton = $("#banButton")
    var banEndDateDiv = $("#banEndDate") // Div containing the datepicker in the ban modal
    var banEndDatepicker = $("#banEndDatepicker") // Datepicker in the ban modal
    var banNoteDiv = $("#banNoteDiv") // Div containing the note displaying why the user was banned previously
                                     //Should only diplay when the modal is going to unban a user
    var banNote = $("#banNote")

    banButton.text($(this).val() + " Volunteer");
    banButton.data("programID", $(this).data("programid"))
    banButton.data("username", $(".form-check-input").data("username"))
    banButton.data("banOrUnban", $(this).val());
    banEndDateDiv.show();
    banEndDatepicker.val("")
    $(".modal-title").text($(this).val() + " Volunteer");
    $("#modalProgramName").text("Program: " + $(this).data("name"));
    $("#banModal").modal("toggle");
    banNoteDiv.hide();
    $("#banNoteTxtArea").val("");

    if( $(this).val()=="Unban"){
      banEndDateDiv.hide()
      banEndDatepicker.val("0001-01-01") //This is a placeholder value for the if statement in line 52 to work properly #PLCHLD1
      banNoteDiv.show()
      banNote.text($(this).data("note"))
    }

  });

  $("#banNoteTxtArea, #banEndDatepicker").on('input' , function (e) { //This is the if statement the placeholder in line 45 is for #PLCHLD1
    var enableButton = ($("#banNoteTxtArea").val() && $("#banEndDatepicker").val());
    $("#banButton").prop("disabled", !enableButton);
  });

  $("#banButton").click(function (){
    var username = $(this).data("username") //Expected to be the unique username of a user in the database
    var route = ($(this).data("banOrUnban")).toLowerCase() //Expected to be "ban" or "unban"
    var program = $(this).data("programID") //Expected to be a program's primary ID
    $.ajax({
      method: "POST",
      url:  "/" + username + "/" + route + "/" + program,
      data: {"note": $("#banNoteTxtArea").val(),
             "endDate":$("#banEndDatepicker").val() //Expected to be a date in this format YYYY-MM-DD
            },
      success: function(response) {

        location.reload();
      }
    });
  });


  $(".backgroundCheck").change(function () { // Updates the Background check of a volunteer in the database
    checkType = $(this).attr("id")
    let data = {
        checkPassed : $(this).val(),      // Expected to be either a 0 or a 1
        user: $(this).data("username"),   // Expected to be the username of a volunteer in the database
        bgType: checkType,       // Expected to be the ID of a background check in the database
        bgDate: $("#" + checkType + "_date").val()  // Expected to be the type (ex. FBI) and  _date
    }

    $.ajax({
      url: "/updateBackgroundCheck",
      type: "POST",
      data: data,
      success: function(s){
      },
      error: function(error, status){
          console.log(error, status)
      }

    })

  });

});
