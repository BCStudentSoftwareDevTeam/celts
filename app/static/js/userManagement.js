import searchUser from './searchUser.js'
function callback(selected) {
  $("#searchAdmin").submit();
}

$(document).ready(function() {
  // Admin Management
  var searchElements = [
    ['searchCeltsAdminInput', 'addCeltsAdmin', 'instructor'],
    ['searchCeltsStudentStaffInput', 'addCeltsStudentStaff', 'student'],
    ['removeCeltsAdminInput','removeCeltsAdmin', 'admin'],
    ['removeCeltsStudentStaffInput', 'removeCeltsStudentStaff', 'studentstaff']
  ];
  $.each(searchElements, function(i,arr) {
      let inputId = arr[0]
      let btnId = arr[1]
      let category = arr[2]
      $("#"+inputId).on("input", () => searchUser(inputId, callback, false, null, category))
      $("#"+btnId).on("click", () => submitRequest(btnId, "#"+inputId))
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

  for (var i=1; i<=$('#currentTermList .term-btn').length; i++){
    $("#termFormID_"+i).on("click", function() {
      $(".term-btn").removeClass("active");
      $(this).addClass('active');
    });
  };
  $("#submitButton").on("click", function() {
    submitTerm();
  });
});

function submitRequest(method,identifier) {
  let data = {
      method : method,
      user : $(identifier).val(),
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
  var termInfo = {id: $("#currentTermList .active").val()};
  $.ajax({
    url: "/admin/changeTerm",
    type: "POST",
    data: termInfo,
    success: function(s){
      location.reload()
    },
    error: function(error, status){
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
