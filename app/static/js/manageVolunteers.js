import searchUser from './searchUser.js'

$(document).ready(function() {
  $('[data-toggle="tooltip"]').tooltip();
  $("#addVolunteerModal input[type=checkbox]").click(updateSelectVolunteer);
  $('[data-toggle="previousVolunteerHover"]').popover({
    trigger: "hover",
    sanitize: false,
    html: true,
    content: "Previous Volunteer"
  });

  
  function initializeTable(){
    let tableID = this.id
    let table =  $('#' + tableID).DataTable({
      "fnDrawCallback": function(oSettings) {
        let participantCount = $('#' + tableID).data('entry-count');
        initializeTrainingPopovers();
        $("#" + tableID + " .removeVolunteer").on("click", removeVolunteer); // we need to rebind this as new rows become visible
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


  // Search functionalities from the volunteer table in the UI
    $("#trackVolunteersInput").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#volunteerTable tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });

    function updateSelectVolunteer(){
      let selectedVolunteers = getSelectedVolunteers()
      let buttonContent = $("#addVolunteersButton").html()
      if (selectedVolunteers.length > 1) {
        if (buttonContent.charAt(buttonContent.length-1) != "s") {
          // make the button text plural if there are multiple users selected
          $("#addVolunteersButton").html(buttonContent + "s")
        }
      } else if (buttonContent.charAt(buttonContent.length-1) == "s") {
        // remove the s if it is plural and we have less than 2 volunteers
        $("#addVolunteersButton").html(buttonContent.slice(0, -1))
      }
      // disable the submit button if there are no selectedCheckboxes
      if (selectedVolunteers.length == 0) {
        $("#addVolunteersButton").prop("disabled", true)
      } else {
        $("#addVolunteersButton").prop("disabled", false)
      }

    }
    
    function getSelectedVolunteers() {
      // get all the checkboxes and return a list of users who's
      // checkboxes are selected
      let checkboxesDisplayedInModal = $("#addVolunteerModal input[type=checkbox]")
      let selectedVolunteers = []
      checkboxesDisplayedInModal.each(function(index, checkbox){
        if(checkbox["checked"]){
          selectedVolunteers.push(checkbox["value"])
        }
      })
      return selectedVolunteers
    }

  // Adding the new volunteer to the user database table
    $("#addVolunteersButton").click(function(){
        $("#addVolunteersButton").prop("disabled", true)
        let eventId = $("#eventID").val()
        let selectedVolunteers = getSelectedVolunteers()
        $.ajax({
          url: `/addVolunteersToEvent/${eventId}`,
          type: "POST",
          data: {"selectedVolunteers": selectedVolunteers, "ajax": true},
          success:
          function(s){
              location.reload()
          },
          error: function(request, status, error){
              location.reload()
          }
      })
    })

    var userlist = $(".repeatingVolunteer").map(function(){
      return $(this).val()
    }).get()

      function callback(selected) {
      let user = $("#addVolunteerInput").val()

      // Check if user is already in the list
      if (userlist.includes(selected["username"])) {
        msgFlash("User already selected.")
        return;
      }

      // Check banned status BEFORE adding user
      let eventId = $("#eventID").val();
      $.ajax({
        url: `/addVolunteersToEvent/${selected["username"]}/${eventId}/isBanned`,
        type: "GET",
        success: function(response) {
          if (response.banned) {
            msgToast("Error", "This user is banned from this program and cannot be added.", 5000);
            return; 
          }
          
          // User is not banned, proceed to add them
          addUserToList(user, selected);
        },
      });
    }

    // Helper function to add user to the list
    function addUserToList(user, selected) {
      userlist.push(user);
      let i = userlist.length;
      $("#addVolunteerList").prepend("<li class id= 'addVolunteerElements"+i+"'> </li>");          
      $("#addVolunteerElements"+i).append("<input type='checkbox' id= 'userlistCheckbox"+i+"' checked value='" + user +"' >");
      $("#addVolunteerElements"+i).append("<label for= 'userlistCheckbox"+i+"'>"+ selected["firstName"]+ " " + selected["lastName"] +"</label>");
      $("#userlistCheckbox"+i).click(updateSelectVolunteer);
      updateSelectVolunteer();
    }

  $("#addVolunteersButton").prop('disabled', true);

  $("#addVolunteerModal").on("shown.bs.modal", function() {
      $('#addVolunteerInput').focus();
  });

  $("#addVolunteerInput").on("input", function() {
    searchUser("addVolunteerInput", callback, true, "addVolunteerModal");
  });


  function removeVolunteer(){
    $(".removeVolunteer").prop("disabled", true)
    let username =  this.id;
    let eventId = $('#eventID').val()
    $.ajax({
      url: '/removeVolunteerFromEvent',
      type: "POST",
      data: {username: username, eventId: eventId},
      success: function(response) {
         location.reload();
      },
      error: function(request, status, error) {
          $(".removeVolunteer").prop("disabled", false)
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

  $("#selectAllVolunteers").click(function(){
      $("#addVolunteerModal input[type=checkbox]").prop('checked', true);
      updateSelectVolunteer();
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
});