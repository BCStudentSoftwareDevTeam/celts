import searchUser from './searchUser.js'

$(document).ready(function() {
  $('[data-toggle="tooltip"]').tooltip();
  var iconShowing = false

  $("#addLaborModal input[type=checkbox]").click(updateSelectLabor);
  $('[data-toggle="previousLaborHover"]').popover({
    trigger: "hover",
    sanitize: false,
    html: true,
    content: "Previous Labor"
  });

  
  function initializeTable(){
    let tableID = this.id
    let table =  $('#' + tableID).DataTable({
      "fnDrawCallback": function(oSettings) {
        let participantCount = $('#' + tableID).data('entry-count');
        initializeTrainingPopovers();
        $("#" + tableID + " .removeLabor").on("click", removeLabor); // we need to rebind this as new rows become visible
        let displayedRows = $('#' + tableID + ' tr').length; // This is actually the number of displayed particpants plus one extra row for the column labels
        if (displayedRows > participantCount){
          $('#' + tableID + '_paginate').hide();
        }
        else{
          $('#' + tableID + '_paginate').show();
        }
      },
      "language": {
        "emptyTable": "No Records Found"
      }
    });
    let participantCount = $('#' + tableID).data('entry-count');
    if (participantCount < 11){
      $('#' + tableID + '_length').hide();
    }
  }
  $("table").each(initializeTable)


  // Search functionalities from the labor table in the UI
    $("#trackLaborInput").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#laborTable tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });

    function updateSelectLabor(){
      let selectedLabor = getSelectedLabor()
      let buttonContent = $("#addLaborButton").html()
      if (selectedLabor.length > 1) {
        if (buttonContent.charAt(buttonContent.length-1) != "s") {
          // make the button text plural if there are multiple users selected
          $("#addLaborButton").html(buttonContent + "s")
        }
      } else if (buttonContent.charAt(buttonContent.length-1) == "s") {
        // remove the s if it is plural and we have less than 2 laborers
        $("#addLaborButton").html(buttonContent.slice(0, -1))
      }
      // disable the submit button if there are no selectedCheckboxes
      if (selectedLabor.length == 0) {
        $("#addLaborButton").prop("disabled", true)
      } else {
        $("#addLaborButton").prop("disabled", false)
      }

    }
    
    function getSelectedLabor() {
      // get all the checkboxes and return a list of users who's
      // checkboxes are selected
      let checkboxesDisplayedInModal = $("#addLaborModal input[type=checkbox]")
      let selectedLabor = []
      checkboxesDisplayedInModal.each(function(index, checkbox){
        if(checkbox["checked"]){
          selectedLabor.push(checkbox["value"])
        }
      })
      return selectedLabor
    }

  // Adding the new labor to the user database table
    $("#addLaborButton").click(function(){
        $("#addLaborButton").prop("disabled", true)
        let eventId = $("#eventID").val()
        let selectedLabor = getSelectedLabor()
        $.ajax({
          url: `/addLaborToEvent/${eventId}`,
          type: "POST",
          data: {"selectedLabor": selectedLabor, "ajax": true},
          success:
          function(s){
              location.reload()
          },
          error: function(request, status, error){
              location.reload()
          }
      })
    })

    var userlist = $(".repeatingLabor").map(function(){
      return $(this).val()
    }).get()
    function callback(selected) {
      let user = $("#addLaborInput").val()
      if (userlist.includes(selected["username"]) == false){
          userlist.push(user)
          let i = userlist.length;
          $("#addLaborList").prepend("<li class id= 'addLaborElements"+i+"'> </li>")          
          $("#addLaborElements"+i).append("<input  type='checkbox' id= 'userlistCheckbox"+i+"' checked value='" + user +"' >  </input>")
          $("#addLaborElements"+i).append("<label form for= 'userlistCheckbox"+i+"'>"+ selected["firstName"]+ " " + selected["lastName"] +"</label>")
          handleBanned(selected["username"], $("#eventID").val(), i)
          $("#userlistCheckbox"+i).click(updateSelectLabor)
          updateSelectLabor()
      }
      else {
          msgFlash("User already selected.")
      }
    }
  $("#addLaborButton").prop('disabled', true);
+
  $("#addLaborModal").on("shown.bs.modal", function() {
      $('#addLaborInput').focus();
  });

  $("#addLaborInput").on("input", function() {
    searchUser("addLaborInput", callback, true, "addLaborModal");
  });


  function removeLabor(){
    $(".removeLabor").prop("disabled", true)
    let username =  this.id;
    let eventId = $('#eventID').val()
    let fullName = $(`#${username}FullName`).text();    

    $.ajax({
      url: '/removeLaborFromEvent',
      type: "POST",
      data: {username: username, eventId: eventId, fullName: fullName,},
      success: function(response) {
         location.reload();
      },
      error: function(request, status, error) {
          $(".removeLabor").prop("disabled", false)
      }
    });
  }

  $("#addRsvpFromWaitlistBtn").on("click",function(){
    let username = $('#addRsvpFromWaitlistBtn').val()
    let eventId = $('#eventID').val()
    $.ajax({
      url: `/rsvpFromWaitlist/${username}/${eventId}`,
      type: "POST",
      success: function(s) {
         location.reload();
      }
    });
  });


  $(".attendanceCheck").on("change", function() {
    let username =  this.name.substring(9) //get everything after the 9th character;
    let inputFieldID = `inputHours_${username}`

    if (this.checked) {
      $(`#${inputFieldID}`).prop('disabled', false);
      let eventLength = $("#eventLength").text();
      $(`#${inputFieldID}`).val(eventLength);

    } else {
      $(`#${inputFieldID}`).prop('disabled', true);
      $(`#${inputFieldID}`).val(null);
    }
  });

  $("#selectAllLabor").click(function(){
      $("#addLaborModal input[type=checkbox]").prop('checked', true);
      updateSelectLabor();
  });

  function initializeTrainingPopovers(){
    $(".trainingPopover").popover({
      trigger: "hover",
      sanitize: false,
      html: true,
      content: function() {
          return $(this).attr('data-content');
      }
    });
  }
  

  function handleBanned(username, eventId, index){
    $.ajax({
      url: `/addLaborToEvent/${username}/${eventId}/isBanned`,
      type: "GET",
      success: function(response){
        if (response.banned){
          $("#addLaborElements"+index).append("<a href='#' data-toggle='tooltip' data-placement='top' title='User is banned from this program.'><span class='bi bi-x-circle-fill text-danger'></span></a>")
          if (!iconShowing){
            $("#banned-message").removeAttr("hidden")
            iconShowing = true
          }
        }
      },
      error: function(request, status, error){
          console.log(status, error)
      }
    })
  }
});