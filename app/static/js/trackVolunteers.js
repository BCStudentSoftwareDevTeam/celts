import searchUser from './searchUser.js'

$(document).ready(function() {
  var table =  $('#trackVolunteerstable').DataTable({
  "fnDrawCallback": function(oSettings) {
    if ($('#trackVolunteerstable tr').length < 11) {
        $('.dataTables_paginate').hide(); //disable search and page numbers when the length of the table is less 11
        $('.dataTables_filter').hide();
        $('.dataTables_length').hide();
      }
    }
  });

  $('[data-toggle="tooltip"]').tooltip();

  // Search functionalities from the volunteer table in the UI
    $("#trackVolunteersInput").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#volunteerTable tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });


  // Adding the new volunteer to the user database table
    $("#selectVolunteerButton").click(function(){
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
          data: {"volunteer" :volunteerList, "ajax": true},
          success: function(s){
              location.reload()
          },
          error: function(request, status, error){
              location.reload()
          }
      })
    })

    var userlist = []
    function callback(selected) {
      $("#selectVolunteerButton").prop('disabled', false);
      let user = $("#addVolunteerInput").val()
      if(userlist.includes(selected["username"]) == false){
          userlist.push(user)
          let i = userlist.length;
          $("#addVolunteerList").append("<li class id= 'addVolunteerElements"+i+"'> </li>")
          $("#addVolunteerElements"+i+"").append("<input  type='checkbox' id= 'userlistCheckbox"+i+"' checked value='" + user +"' >  </input>")
          $("#addVolunteerElements"+i+"").append("<label form for= 'userlistCheckbox"+i+"'>"+ selected["firstName"]+ " " + selected["lastName"] +"</label>")
      }
      else{
          msgFlash("User already selected.")
      }
    }
  $("#selectVolunteerButton").prop('disabled', true);

  $("#addVolunteerInput").on("input", function() {
    searchUser("addVolunteerInput", callback, true, "addVolunteerModal");
  });

  $(".removeVolunteer").on("click", function() {
    let username =  this.id;
    let eventId = $('#eventID').val()
    $.ajax({
      url: `/removeVolunteerFromEvent/${username}/${eventId}`,
      type: "POST",
      success: function(s) {
         location.reload();
      },
      error: function(request, status, error) {
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
      $("#addPastVolunteerModal input[type=checkbox]").prop('checked', true)
  });
});
