import searchUser from './searchUser.js'

function callbackAdmin(selected){
    submitRequest("addCeltsAdmin", selected.username)
}
function callbackStudentStaff(selected){
    submitRequest("addCeltsStudentStaff", selected.username)
}
$(document).ready(function(){
  // Admin Management
  $("#searchCeltsAdminInput").on("input", function(){
      searchUser("searchCeltsAdminInput", callbackAdmin, false, null, "celtsLinkAdmin")
  });
  $("#searchCeltsStudentStaffInput").on("input", function(){
      searchUser("searchCeltsStudentStaffInput", callbackStudentStaff, false, null, "student")
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
//################UPDATE THE MODAL##################
export function populateModal(programName, programDescription, modalprogramImage, partner, contactEmail, contactName, location, programId) {
  /* Update modal fields with program information*/

  document.getElementById('programName').value = programName;
  document.getElementById('programDescription').value = programDescription;
  document.getElementById('modalProgramImage').setAttribute('data-current-file', modalprogramImage);
  document.getElementById('modalProgramImage').addEventListener('change', function(e){
    const file = e.target.files[0];
    if (file){
      msgFlash("Image added!", "success");
      document.getElementById('modalProgramImage').setAttribute('data-selected-file', file.name);
      console.log("New file ", file);
    }
  });
  document.getElementById('partner').value = partner;
  document.getElementById('contactEmail').value = contactEmail;
  document.getElementById('contactName').value = contactName;
  document.getElementById('location').value = location;
  //console.log(modalprogramImage);

  //update the form action URL based on the program selected
  let updateForm = document.getElementById('updateProgramForm')
  updateForm.action = "/admin/updateProgramInfo/" + programId;
}
// Ensure all modals close when clicking outside of them 
document.addEventListener('click', function(event) {
  var isClickInside = document.getElementById('adminProgramManagement').contains(event.target);
  if (!isClickInside) {
     document.getElementById('adminProgramManagement').classList.remove('show');
  }
});
//################SUBMIT TERM##################
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
