import searchUser from './searchUser.js'

function callbackAdmin(selected){
    submitRequest("addCeltsAdmin", selected.username)
}
function callbackStudentStaff(selected){
    submitRequest("addCeltsStudentStaff", selected.username)
}

function callbackProgramManager(selected, action = 'add') {
  let row = $(`#programManagersTable tr[username="${selected["username"]}"]`);
  let exists = row.length > 0;
  let programId = $('#programPlaceholder').attr('data-programid');

  if (action === 'remove' || (!exists && action === 'add')){
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
      searchUser("searchCeltsAdminInput", callbackAdmin, false, null, "celtsLinkAdmin")
  });
  $("#searchCeltsStudentStaffInput").on("input", function(){
      searchUser("searchCeltsStudentStaffInput", callbackStudentStaff, false, null, "student")
  });
  $("#searchProgramManagersInput").on("input", function() {
      searchUser("searchProgramManagersInput", callbackProgramManager, true, "parentManager", "student");
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
  $('[data-bs-target="#adminProgramManagement"]').on('click', function() {
    // Get the JSON data from the data-programinfo attribute
    const programInfo = JSON.parse($(this).attr('data-programinfo'));
    // Directly populate modal fields
    $("#programName").val(programInfo.programName);
    $("#programDescription").val(programInfo.programDescription);
    $("#partner").val(programInfo.partner);
    $("#contactEmail").val(programInfo.contactEmail);
    $("#contactName").val(programInfo.contactName);
    $("#location").val(programInfo.location);
    $("#programid").val(programInfo.programid)
    $("#instagramUrl").val(programInfo.instagramUrl);
    $("#facebookUrl").val(programInfo.facebookUrl);
    $("#bereaUrl").val(programInfo.bereaUrl);
    $('#modalProgramImage').val('');
    $('#modalProgramImageContainer').html('');

    handleFileSelection('modalProgramImage', true);
    // Update the form action URL dynamically
    let updateForm = $('#updateProgramForm');
    updateForm.attr('action', "/admin/updateProgramInfo/" + programInfo.programid);
    });

    $('[data-bs-target="#editProgramManagers"]').on('click', function(){
      const managers = $(this).attr('data-managers').split(',');
      const managersTable = $('#programManagersTable');

      managersTable.empty();
      
      if(managers[0].length == 0){
        return;
      };

      managers.forEach(manager => {
        let [managerName, managerUser] = manager.split('#');
        managersTable.append(createProgramManagerRow(managerUser, managerName))
      });
    })

    $('.editProgramManagersButton').on('click', function(){
      $('#programPlaceholder').attr('data-programid', $(this).attr('data-programid'));
      $('#programNameHeader').html(`Edit ${$(this).attr('data-name')} Managers`)
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
      user_name: username,
      program_id: programId,
      action: action,
  }
  $.ajax({
    url: "/updateProgramManager",
    type: "POST",
    data: data,
    success: function(s){
      if (action === 'add'){
        $('#programManagersTable').append(createProgramManagerRow(username, fullName))
        updateManagers()
      } else {
        $(`#programManagersTable #${username}`)
        .animate({
          opacity: 0,
        }, 500, function() {
          $(`#programManagersTable #${username}`)
          .closest('tr')
          .remove()
          updateManagers()
        })
      }
    },
    error: function(error, status){
      console.log(error, status)
      msgFlash('Task failed. Please try again')
    }
  })
}

function updateManagers(){
  let newManagers = []
  let username = ""
  let fullName = "";
  $("#programManagersTable").children().each((index, manager) => {
    username = $(manager).find("td:first-child").attr("id");
    fullName = $(manager).find("td:first-child").html().trim();
    newManagers.push(`${fullName}#${username}`);
  });
  let managersString = newManagers.join(",");
  $("#editProgramManagersButton").attr('data-managers', managersString)
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
