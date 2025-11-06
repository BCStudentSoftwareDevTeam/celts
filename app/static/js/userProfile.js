$(document).ready(function(){

  $("#checkDietRestriction").on("change",  function() {
    let norestrict = $(this).is(':checked');
    if (norestrict) {
        $("#dietContainer").hide();
        $("#diet").val("No dietary restrictions");

    } else {
        $("#dietContainer").show();
    }
  });

  $("#checkIsInterest").on("change", function() {
    let username = $(this).data('username')
    let isAdding = $(this).is(':checked');

    $.ajax({
        url: "/profile/"+username+"/indicateInterest",
        type: "POST",
        data: JSON.stringify({ "isAdding": isAdding }),
        contentType: "application/json",
        success: function(response) {
          let accept = "You have indicated interest in CCE Minor.";
          let decline = "You have indicated you are not interested in the CCE Minor.";
       
          let msg = isAdding ? accept : decline;
          msgToast('Success', msg);
          $("#interestIndicatedText").text(msg);
        },
        error: function(request, status, error) {
          console.log(status, error)
          msgToast("Error!","Failed to save changes!")
        }
    });
  })

  // var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  // var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  //   return new bootstrap.Tooltip(tooltipTriggerEl)
  // })
  
  // $("#printButton").on("click", function() {
  //       let username = $(this).data('username')
  //       printDocument(`/profile/${username}/travelForm`)
  //     })
  // $("#actions").on("change", changeAction)
  // $("#phoneInput").inputmask('(999)-999-9999');
  $(".notifyInput").click(function updateInterest(){
    var programID = $(this).data("programid");
    var username = $(this).data('username');


    var interest = $(this).is(':checked');
    var routeUrl = interest ? "addInterest" : "removeInterest";
    interestUrl = "/" + username + "/" + routeUrl + "/" + programID ;
    $.ajax({
      method: "POST",
      url: interestUrl,
      success: function(response) {
          reloadWithAccordion("programTable")  //  Reloading page after user clicks on the show interest checkbox
      },
      error: function(request, status, error) {
        console.log(status,error);
        location.reload();
      }
    });
  });

  $('.onTranscriptCheckbox').click(function() {
    var onTranscript = $(this).is(':checked');
    var username = $(this).data('username');
    var programID = $(this).data("programid");
    displayTranscriptStatus(programID);
   
    $.ajax({
        type: "POST",
        url: `/profile/${username}/updateTranscript/${programID}`,
        contentType: "application/json",
        data: JSON.stringify({ username: username, removeFromTranscript: !onTranscript, programID: programID }),
        success: function(response) {

        },
        error: function(error) {
            console.error("An error occurred:", error);
        }
    });

  });

  function displayTranscriptStatus(programID) {
    $('#transcriptStatus-' + programID).show();
    $('#transcriptStatus-' + programID).text("Saved!");
    $('#transcriptStatus-' + programID).css('color', 'blue');
    //show for 0.5s and fade out last for 0.5s
    setTimeout(function() {
      $('#transcriptStatus-' + programID).fadeOut(500, function() {
          $(this).text('');
      });
    }, 500);
  }

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

    /*
     * Ban Functionality
     */
  $(".banEdit").click(function() {
    var banButton = $("#banButton")
    var banEndDateDiv = $("#banEndDate") // Div containing the datepicker in the ban modal
    var banEndDatepicker = $("#banEndDatepicker") // Datepicker in the ban modal
    var banNoteDiv = $("#banNoteDiv") // Div containing the note displaying why the user was banned previously
    banNoteDiv.hide();                //Should only diplay when the modal is going to unban a user
    var banNote = $("#banNote")
    var banValue = $(this).val()

    banButton.text(banValue + " Volunteer");
    programID = $(this).data("programid"); // Assign value to programID variable
    banButton.data("programID", programID)
    banButton.data("username", $(".banEdit").data("username"))
    banButton.data("banOrUnban", banValue);
    banEndDateDiv.show();
    banEndDatepicker.val("")
    $(".modal-title-ban").text(banValue + " Volunteer from "+ $(this).data("name") + "?");
    $("#modalProgramName").text("Program: " + $(this).data("name"));
    $("#banModal").modal("toggle");
    $("#banNoteTxtArea").val("");
    $("#banButton").prop("disabled", true);
    if(banValue == "Unban"){
      banEndDateDiv.hide()
      banEndDatepicker.val("0001-01-01") //This is a placeholder value for the if statement in line 52 to work properly #PLCHLD1
      banNoteDiv.show()
      banNote.text($(this).data("note"))
    }
   
  });

  $("#banNoteTxtArea, #banEndDatepicker").on('input change' , function (e) { //This is the if statement the placeholder in line 45 is for #PLCHLD1
    var enableButton = ($("#banNoteTxtArea").val() && $("#banEndDatepicker").val());
    $("#banButton").prop("disabled", !enableButton);
  });

  $("#banButton").click(function (){
     $("#banButton").prop("disabled", true)
    var username = $(this).data("username") //Expected to be the unique username of a user in the database
    var route = ($(this).data("banOrUnban")).toLowerCase() //Expected to be "ban" or "unban"
    var program = $(this).data("programID") //Expected to be a program's primary ID
   
    $.ajax({
      method: "POST",
      url:  "/" + username + "/" + route + "/" + program,
      data: {"note": $("#banNoteTxtArea").val(),
             "endDate":$("#banEndDatepicker").val(), //Expected to be a date in this format YYYY-MM-DD
            },
      success: function(response) {
        reloadWithAccordion("programTable")
      }
    });
  });

    /*
     * Note Functionality
     */
    function bonnerNoteOff() {
        $("#bonnerInput").prop("checked", false);
        $("#noteDropdown").show()
        $("#bonnerStatement").hide()
        $("#visibilityLabel").show()
    }

    function bonnerNoteOn() {
        $("#bonnerInput").prop("checked", true);
        $("#noteDropdown").hide()
        $("#bonnerStatement").show()
        $("#visibilityLabel").hide()
    }

    $("#addNoteButton").click(function() {
        bonnerNoteOff()
        $("#noteModal").modal("toggle")
    });

    $("#addVisibility").click(function() {
        var bonnerChecked = $("input[name='bonner']:checked").val()

        if (bonnerChecked == 'on') {
            bonnerNoteOn()
        } else {
            bonnerNoteOff()
        }
    });

    $("#addBonnerNoteButton").click(function() {
        bonnerNoteOn()
        $("#noteModal").modal("toggle");
    });

  $('#addNoteForm').submit(function(event) {

    event.preventDefault()
    let username = $("#notesSaveButton").data('username')
    let isBonner = $("#bonnerInput").is(":checked")
    $.ajax({
      method: "POST",
      url:  "/profile/addNote",
      data: {"username": username,
             "visibility": $("#noteDropdown").val(),
             "noteTextbox": $("#addNoteTextArea").val(),
             "bonner": isBonner ? "yes" : "no"},
      success: function(response) {
          target = isBonner ? "bonner" : "notes"
          msgFlash("Successfully added a note", "success", 1300, true);
          location.reload()
      },
      error: function(error) {
        console.log("error")
      }
    });
  });
  });


  $(".deleteNoteButton").click(function() {
    let username = $(this).data('username')
    let noteid = $(this).data('noteid')
    $.ajax({
      method: "POST",
      url:  "/" + username + "/deleteNote",
      data: {"id": noteid},
      success: function(response) {
        reloadWithAccordion("notes")
      }
    });
  });

  /*
    * Background Check Functionality
    */
  // Updates the Background check of a volunteer in the database

  $(".savebtn").click(function () {
    msgFlash()
      enableLiveCustomValidityClearing([".passedBackgroundCheck"])
      $(this).prop("disabled", true);
      let bgCheckType = $(this).data("id")

      var bgStatusInput = $("#" + bgCheckType)
      var bgDateInput = $("#" + bgCheckType + "_date")

      let bgDate =  bgDateInput.val()
      let bgStatus = $("[data-id=" + bgCheckType + "]").val()

        if (bgStatus == '') {
          bgStatusInput.focus()
           $('.form-select').each(function() {
                bgStatusInput[0].setCustomValidity("Please enter a status");
                bgStatusInput[0].reportValidity();
          });
          $(this).prop("disabled", false);
          return false
        }

        if (bgDate == ''){
          bgDateInput.focus()
          $('.form-control').each(function() {
                bgDateInput[0].setCustomValidity("Please enter a date");
                bgDateInput[0].reportValidity();
          });
          $(this).prop("disabled", false);
          return false
        }

        let data = {
            bgStatus: bgStatus,      // Expected to be one of the three background check statuses
            user: $(this).data("username"),   // Expected to be the username of a volunteer in the database
            bgType: $(this).attr("id"),       // Expected to be the ID of a background check in the database
            bgDate: bgDate  // Expected to be the date of the background check completion or '' if field is empty
        }
        $.ajax({
          url: "/addBackgroundCheck",
          type: "POST",
          data: data,
          success: function(s){
            var date = new Date(data.bgDate + " 12:00").toLocaleDateString()
            msgFlash(`Successfully added background check`, "success", 1300,true)
            reloadWithAccordion("background")
          },
          error: function(error, status){
              console.log(error, status)
          }
        })
    });

  $("#bgHistoryTable").on("click", "#deleteBgHistory", function() {
    let data = {
        bgID: $(this).data("id"),       // Expected to be the ID of a background check in the database
    }
    $(this).closest("li").remove();

    $.ajax({
      url: "/deleteBackgroundCheck",
      type: "POST",
      data: data,
      success: function(s){
       msgFlash(`Successfully deleted background check, <a href="/profile/undo" id="bgCheckUndo" class="mx-2">Undo</a>`, "success")
      },        
      error: function(error, status){
        console.log(error,status)
      }
    })
  });

  // Popover functionality
  // var requiredTraining = $(".trainingPopover");
  // requiredTraining.popover({
  //     trigger: "hover",
  //     sanitize: false,
  //     html: true,
  //     content: function() {
  //         return $(this).attr('data-content');
  //     }
  // });
  $(function () {
    $('.trainingPopover').each(function () {
      new bootstrap.Popover(this, {
        trigger: 'hover focus',
        html: true,
        sanitize: false,
        placement: 'right',
      });
    });
  });
  $(function () {
    $('.bonnerCheckmark').each(function () {
      new bootstrap.Popover(this, {
        trigger: 'hover focus',
        html: true,
        sanitize: false,
        placement: 'right',
      });
    });
  });

  setupPhoneNumber("#updatePhone", "#phoneInput")

  // Dietary Restrictions
  function saveDiet() {
    let data = {
      dietInfo: $("#diet").val(),
      user: $("#diet").data("user")
    };
    
    $.ajax({
      type: "POST",
      url: "/updateDietInformation",
      data: data,
      success: function(s) {
        $('#saveNotification').fadeIn('fast').delay(1000).fadeOut('slow');
      }
    });
  }

  $("#checkDietRestriction").on("change",  function() {
    let norestrict = $(this).is(':checked');
    if (norestrict) {
        $("#dietContainer").hide();
        $("#diet").val("No dietary restrictions");
        saveDiet()
    }

    var typingTimer;
    var saveInterval = 1000; //milliseconds

    $("#diet").on('input', function() {
      clearTimeout(typingTimer);
      $('#check-icon').remove();
      
      typingTimer = setTimeout(saveDiet, saveInterval);
    });
  });
  const bonnerStudent = $("#bonnerStudent").data('username')
  if (bonnerStudent === "False"){
    $("#bonnerStudent").prop("hidden", true)
  }; // end document.ready()

// Update program manager status
function updateManagers(el, volunteerUsername ) {
  let programId=$(el).attr('data-programid');
  let programName = $(el).attr('data-programName')
  let name = $(el).attr('data-name')
  let action= el.checked ? 'add' : 'remove';
  let removeMessage = (name + " is no longer the manager of " + programName + ".")
  let addMessage =  (name + " is now the manager of " + programName + ".")

  $.ajax({
    method:"POST",
    url:"/updateProgramManager",
    data : {"username":volunteerUsername,
            "programId":programId,      
            "action":action,          
             },

     success: function(s){
         if(action == "add"){
             msgToast("Program manager", addMessage)
         } else if(action == 'remove'){
             msgToast("Program manager", removeMessage)
         }
      },
      error: function(error, status){
          console.log(error, status)
      }
  })
}

