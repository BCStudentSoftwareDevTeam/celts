import searchUser from './searchUser.js'

$(document).ready(function() {
  $('[data-toggle="tooltip"]').tooltip();
  var iconShowing = false

  $("#addVolunteerModal input[type=checkbox]").click(updateSelectVolunteer);
  $('[data-toggle="previousVolunteerHover"]').popover({
    trigger: "hover",
    sanitize: false,
    html: true,
    content: "Previous Volunteer"
});

var participantCount = $('#trackVolunteerstable').attr('data-entryCount');
  var table =  $('#trackVolunteerstable').DataTable({
    "fnDrawCallback": function(oSettings) {
      $(".removeVolunteer").on("click", removeVolunteer); // we need to rebind this as new rows become visible
      let displayedRows = $('#trackVolunteerstable tr').length; // This is actually the number of displayed particpants plus one extra row for the column labels
      if (displayedRows > participantCount){
        $('.dataTables_paginate').hide();
      }
      else{
        $('.dataTables_paginate').show();
      }
    }
  });
  if (participantCount < 11){
    $('.dataTables_length').hide();
  }


  // Search functionalities from the volunteer table in the UI
    $("#trackVolunteersInput").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#volunteerTable tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });

    function updateSelectVolunteer(){
      $("#addVolunteerModal input[type=checkbox]").each(function(index, checkbox){
          if(checkbox["checked"] == true){
            $("#addVolunteersButton").prop("disabled", false)
            return false
          }
          $("#addVolunteersButton").prop("disabled", true)
      })
    }
    

  // Adding the new volunteer to the user database table
    $("#addVolunteersButton").click(function(){
        $("#addVolunteersButton").prop("disabled", true)
        let user = $("#addVolunteerInput").val()
        let eventId = $("#eventID").val()
        let checkboxlist = $("#addVolunteerModal input[type=checkbox]")
        let volunteerList = []
        $.each(checkboxlist, function(index, checkbox){
            if(checkbox["checked"] == true){
                volunteerList.push(checkbox["value"])
            }
        })
        $.ajax({
          url: `/addVolunteersToEvent/${eventId}`,
          type: "POST",
          data: {"volunteer": volunteerList, "ajax": true},
          success: function(s){
              location.reload()
          },
          error: function(request, status, error){
              location.reload()
          }
      })
    })

    var userlist = $(".recurringVolunteer").map(function(){
      return $(this).val()
    }).get()
    function callback(selected) {
      let user = $("#addVolunteerInput").val()
      if (userlist.includes(selected["username"]) == false){
          userlist.push(user)
          let i = userlist.length;
          $("#addVolunteerList").prepend("<li class id= 'addVolunteerElements"+i+"'> </li>")          
          $("#addVolunteerElements"+i).append("<input  type='checkbox' id= 'userlistCheckbox"+i+"' checked value='" + user +"' >  </input>")
          $("#addVolunteerElements"+i).append("<label form for= 'userlistCheckbox"+i+"'>"+ selected["firstName"]+ " " + selected["lastName"] +"</label>")
          handleBanned(selected["username"], $("#eventID").val(), i)
          $("#userlistCheckbox"+i).click(updateSelectVolunteer)
          updateSelectVolunteer()
      }
      else {
          msgFlash("User already selected.")
      }
    }
  $("#addVolunteersButton").prop('disabled', true);
+
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

  function handleBanned(username, eventId, index){
    $.ajax({
      url: `/addVolunteersToEvent/${username}/${eventId}/isBanned`,
      type: "GET",
      success: function(response){
        if (response.banned){
          $("#addVolunteerElements"+index).append("<a href='#' data-toggle='tooltip' data-placement='top' title='User is banned from this program.'><span class='bi bi-x-circle-fill text-danger'></span></a>")
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
