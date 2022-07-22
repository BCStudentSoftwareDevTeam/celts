import searchUser from './searchUser.js'
function callbackStudentStaff(selected){
    submitRequest("addCeltsStudentStaff", selected.username)
}
$(document).ready(function(){
  // Admin Management
  $("#searchCeltsAdminInput").on("input", function(){
      searchUser("searchCeltsAdminInput", callbackAdmin, false, null, "instructor")
  });
  $("#searchCeltsStudentStaffInput").on("input", function(){
      searchUser("searchCeltsStudentStaffInput", callbackStudentStaff, false, null, "student")
  });
  $("#addNewTerm").on("click",function(){
    addNewTerm();
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
      location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }
  })
}
function addNewProgramInfo(){
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