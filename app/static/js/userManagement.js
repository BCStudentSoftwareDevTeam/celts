import searchUser from './searchUser.js'

function callbackAdmin(selected){
    submitRequest("addCeltsAdmin", selected.username)
}
function callbackStudentStaff(selected){
    submitRequest("addCeltsStudentStaff", selected.username)
}
function callbackProgramManager(selected){
    submitRequest("addProgramManager", selected.username)
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
  $(".removeProgramManager").on("click",function(){
    submitRequest("removeProgramManager", $(this).data("username"));
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
        let row = document.createElement("tr");
        row.innerHTML = `
                        <td id="${managerUser}"> ${managerName} </td>
                        <td class="text-end"><button data-username="${managerUser}" 
                        type="button" class="btn btn-danger removeProgramManager">Remove</button>
                        </td>
                        `;
        managersTable.append(row)
      });
    })

    $('#editProgramManagersButton').on('click', function(){
      const programId = $(this).attr('data-programid');
      $('#updateProgramForm').append('programId', programId);
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
