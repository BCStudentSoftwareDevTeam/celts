import searchUser from './searchUser.js'
function callbackAdmin(selected) {
    submitRequest("addCeltsAdmin", selected.username)
}
function callbackStudentStaff(selected) {
    submitRequest("addCeltsStudentStaff", selected.username)
}

$(document).ready(function() {
  // Admin Management
  var searchElements = [
    // Search Input ID               Button ID                 Category
    ['searchCeltsAdminInput',       'addCeltsAdmin',          'instructor'],
    ['searchCeltsStudentStaffInput','addCeltsStudentStaff',   'student'],
    ['removeCeltsAdminInput',       'removeCeltsAdmin',       'admin'],
    ['removeCeltsStudentStaffInput','removeCeltsStudentStaff','studentstaff']
  ];
  $.each(searchElements, function(i,arr) {
      let [inputId, btnId, category] = arr
      if (inputId == "searchCeltsAdminInput") {
        $("#"+inputId).on("input", () => searchUser(inputId, callbackAdmin, false, null, category))
    } else {
        $("#"+inputId).on("input", () => searchUser(inputId, callbackStudentStaff, false, null, category))
    }
  });

  $("#addNewTerm").on("click",function(){
    addNewTerm();
  });
  $("#addNewProgramInfo").on("click",function(){
    addNewProgramInfo();
  });
  $("#programSelect").on("change",function(){
    displayProgramInfo();
  });
  $(".removeAdmin").on("click",function(){
    submitRequest("removeCeltsAdmin", $(this).data("username"));
  });
  $(".removeStudentStaff").on("click",function(){
    submitRequest("removeCeltsStudentStaff", $(this).data("username"));
  });
  $('#searchCeltsAdminInput').keydown(function(e) {
      if (e.key === "Enter") {
          submitRequest("addCeltsAdmin", $(this).val())
      }
  });
  $('#searchCeltsStudentStaffInput').keydown(function(e) {
      if (e.key === "Enter") {
          submitRequest("addCeltsStudentStaff", $(this).val())
      }
  });


  for (var i=1; i<=$('#currentTermList .term-btn').length; i++){
    $("#termFormID_"+i).on("click", function() {
      $(".term-btn").removeClass("active");
      $(this).addClass('active');
    });
  };
  $(".term-btn").on("click", function() {
    submitTerm();
  });
});

function submitRequest(method, username) {
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

function submitTerm() {
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

function addNewTerm() {
  $.ajax({
    url: "/admin/addNewTerm",
    type: "POST",
    success: function(s){
      location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }
  })
}

function addNewProgramInfo() {
  var programInfo = {emailSenderName: $("#emailSenderName").val(),
                    emailReplyTo: $("#emailReplyTo").val(),
                    programId: $("#programSelect").val()};
  $.ajax({   // sends ajax request to controller with programInfo containing user input
    url: "/admin/updateProgramInfo",
    type: "POST",
    data: programInfo,
    success: function(s){
      msgFlash("Successfully updated program info", "success")
    },
    error: function(error, status){
        console.log(error, status);
    }
  })
}

function displayProgramInfo(){
  var programInfo = $("#programSelect option:selected")[0]
  $("#emailReplyTo").val($(programInfo).data("replytoemail"))
  $("#emailSenderName").val($(programInfo).data("sendername"))

}
