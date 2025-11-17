import searchUser from './searchUser.js'

var newManagers = []  // global var

function callbackAdmin(selected){
    submitRequest("addCeltsAdmin", selected.username)
}
function callbackStudentStaff(selected){
    submitRequest("addCeltsStudentStaff", selected.username)
}

function callbackProgramManager(selected, action = 'add') {
  let row = $(`#programManagersTable tr[data-username="${selected["username"]}"]`);
  let userDoesNotExist = row.length === 0;
  let programId = $('#programPlaceholder').data('programid');

  if ((action === 'remove') || (userDoesNotExist && action === 'add')){
    editProgramManager(
      selected['username'],
      `${selected['firstName'] + ' ' + selected['lastName']}`,
      programId,
      action
    );
  } else {
    return;
  }
}

$(document).ready(function(){
  // Admin Management
  $("#searchCeltsAdminInput").on("input", function(){
      searchUser("searchCeltsAdminInput", callbackAdmin, false, false, null, "celtsLinkAdmin")
  });
  $("#searchCeltsStudentStaffInput").on("input", function(){
      searchUser("searchCeltsStudentStaffInput", callbackStudentStaff, false, false, null, "student")
  });
  $("#searchProgramManagersInput").on("input", function() {
      searchUser("searchProgramManagersInput", callbackProgramManager, false, true, "parentManager", "all");
  });
  $("#addNewTerm").on("click",function(){
    addNewTerm();
  });
  $(".removeAdmin").on("click",function(){
    submitRequest("removeCeltsAdmin", $(this).data("username"));
  });
  $(".removeStudentStaff").on("click",function(){
    submitRequest("removeCeltsStudentStaff", $(this).data("username"));
  });
  $("#programManagersTable").on("click", ".removeProgramManager", function(){
    let row = $(this).closest("tr");
    let fullName = row.find("td").eq(0).text().trim();
    let [firstName, lastName] = fullName.split(" ");
    callbackProgramManager({
      username: row.data("username"),
      firstName: firstName,
      lastName: lastName
    }, "remove");
    });
  
  $('#searchCeltsAdminInput').keydown(function(e){
      if (e.key === "Enter"){
          submitRequest("addCeltsAdmin", $(this).val())
      }
  });
  $('#searchCeltsStudentStaffInput').keydown(function(e){
      if (e.key === "Enter"){
          submitRequest("addCeltsStudentStaff", $(this).val())
      }
  });

  for (var i = 1; i <= $('#currentTermList .term-btn').length; i++){
    $("#termFormID_" + i).on("click", function(){
      $(".term-btn").removeClass("active");
      $(this).addClass('active');
    });
  };
  $(".term-btn").on("click", function(){
    submitTerm();
  });

  $('.editDetails').on('click', function() {
    const programid = $(this).data('programid')
    const buttonId = $(this).attr('id')
    const buttonTextId = 'editDetailsButtonText' + $(this).attr('loop-index')
    const loadingSpinnerId = 'editDetailsButtonSpinner' + $(this).attr('loop-index')

    // Disable button and make it spin
    $('#' + buttonTextId).hide()
    $('#' + loadingSpinnerId).show()
    $('#' + buttonId).prop( "disabled", true );

    $.ajax({
        method: 'GET',
        url: "/admin/getProgramInfo/" + programid,     
        success: function(response) {
          const programInfo = response[0]

           // Populate the form with the existing data that was retrieved from the AJAX request
          $("#programName").val(programInfo.programName);
          $("#programDescription").val(programInfo.programDescription);
          $("#partner").val(programInfo.partner);
          $("#contactEmail").val(programInfo.contactEmail);
          $("#contactName").val(programInfo.contactName);
          $("#location").val(programInfo.defaultLocation);
          $("#programid").val(programInfo.programid)
          $("#instagramUrl").val(programInfo.instagramUrl);
          $("#facebookUrl").val(programInfo.facebookUrl);
          $("#bereaUrl").val(programInfo.bereaUrl);
          $('#modalProgramImage').val('');
          $('#modalProgramImageContainer').html('');

          handleFileSelection('modalProgramImage', true);

          // Update the form action URL dynamically
          let updateForm = $('#updateProgramForm');
          updateForm.attr('action', "/admin/updateProgramInfo/" + programid);

          // Openning the modal after the data was received
          let modal = new bootstrap.Modal($('#adminProgramManagement'));
          modal.show();

          // Remove the loading spinner after the modal is open
          $('#' + buttonTextId).show()
          $('#' + loadingSpinnerId).hide()
          $('#' + buttonId).prop( "disabled", false );
        }, 
        error: function () {          
            console.error("Failed to retrieve program info", error);
            msgToast("Could not retrieve program info. Please contact <a href='mailto:support@bereacollege.onmicrosoft.com'>Systems Support </a>")
        }
    });
  });

  $(".editProgramManagersButton").on('click', function(){
    $('#programPlaceholder').data('programid', $(this).data('programid'))
    $('#programNameHeader').html(`Edit ${$(this).attr('data-name')} Managers`);

    $('#noManagersText').addClass("d-none")
    const managers = $(this).attr('data-managers').split(',');
    const managersTable = $('#programManagersTable');
    managersTable.empty();
    
    if(managers[0].length == 0){
      $('#noManagersText').removeClass("d-none")
      return;
    };

    managers.forEach(manager => {
      let [managerName, managerUser] = manager.split('#');
      managersTable.append(createProgramManagerRow(managerUser, managerName))
    });
  })
  });

function submitRequest(method, username){
  let data = {
      method: method,
      user: username,
      from: "ajax"
  }
  $.ajax({
    url: "/admin/manageUsers",
    type: "POST",
    data: data,
    success: function(s){
        location.reload()
    },
    error: function(error, status){
      location.reload()
      console.log(error, status)
    }
  })
}

function createProgramManagerRow(username, fullName) {
  return `
      <tr data-username="${username}">
      <td id="${username}"> ${fullName} </td>
      <td class="text-end">
          <button data-username="${username}" type="button" 
          class="btn btn-danger removeProgramManager">Remove</button>
      </td>
      </tr>
  `;
}

function editProgramManager(username, fullName, programId, action){
  let data = {
      username: username,
      programId: programId,
      action: action,
  }
  $.ajax({
    url: "/updateProgramManager",
    type: "POST",
    data: data,
    success: function(s){
      if (action === 'add'){
        $('#noManagersText').addClass("d-none")
        $('#programManagersTable').append(createProgramManagerRow(username, fullName))
        updateManagers(programId)
        msgToast("Confirmed", "You have just added a new program manager")
      } else {
        $(`#programManagersTable #${username}`)
        .animate({
          opacity: 0,
        }, 500, function() {
          $(`#programManagersTable #${username}`)
          .closest('tr')
          .remove()
          msgToast("Confirmed", "You have just deleted a program manager")
          updateManagers(programId)

          if (!(newManagers.length)){
            $('#noManagersText').removeClass("d-none")
          }
        })
      }
    },
    error: function(error, status){
      console.log(error, status)
      msgFlash('Failed to update the Program Manager Table. Please try again')
    }
  })
}

function updateManagers(programId){
  newManagers.length = 0;
  let username = ""
  let fullName = "";
  $("#programManagersTable").children().each((index, manager) => {
    username = $(manager).find("td:first-child").attr("id");
    fullName = $(manager).find("td:first-child").html().trim();
    newManagers.push(`${fullName}#${username}`);
  });
  let managersString = newManagers.join(",");
  $(`.editProgramManagersButton[data-programid='${programId}'`).attr('data-managers', managersString)
}

function submitTerm(){
  var selectedTerm = $("#currentTermList .active")
  var termInfo = {id: selectedTerm.val()};
  $.ajax({
    url: "/admin/changeTerm",
    type: "POST",
    data: termInfo,
    success: function(s){
      msgFlash("Current term successfully changed to " + selectedTerm.html(), "success")
    },
    error: function(error, status){
        msgFlash("Current term was not changed. Please try again.", "warning")
        console.log(error, status)
    }
  })
}

function addNewTerm(){
  $.ajax({
    url: "/admin/addNewTerm",
    type: "POST",
    success: function(s){
      reloadWithAccordion("term")
    },
    error: function(error, status){
        console.log(error, status)
    }
  })
}
