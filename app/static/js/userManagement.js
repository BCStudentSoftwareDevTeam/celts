import searchUser from './searchUser.js'


$(document).ready(function() {
  // add celts admin
  function callback(selected) {
    $("#searchAdmin").submit();
  }

  $("#searchCeltsAdminInput").on("input", function() {
    searchUser("searchCeltsAdminInput", callback);
  });

  $("#addCeltsAdmin").on("click", function() {
    submitRequest("addCeltsAdmin","#searchCeltsAdminInput")
  });

  $("#addNewTerm").on("click",function(){
    addNewTerm();
  });
  $("#programSelect").on("change",function(){
    displayProgramInfo();
  });

  // add celts student staff
  $("#searchCeltsStudentStaffInput").on("input", function() {
    searchUser("searchCeltsStudentStaffInput", callback);
  });

  $("#addCeltsStudentStaff").on("click", function() {
    submitRequest("addCeltsStudentStaff","#searchCeltsStudentStaffInput")
  });

  // remove celts admin
  $("#removeCeltsAdminInput").on("input", function() {
    searchUser("removeCeltsAdminInput", callback);
  });

  $("#removeCeltsAdmin").on("click", function() {
    submitRequest("removeCeltsAdmin","#removeCeltsAdminInput")
  });

  // remove celts student staff
  $("#removeCeltsStudentStaffInput").on("input", function() {
    searchUser("removeCeltsStudentStaffInput", callback);
  });

  $("#removeCeltsStudentStaff").on("click", function() {
    submitRequest("removeCeltsStudentStaff", "#removeCeltsStudentStaffInput")
  });
  for (var i=1; i<=$('#currentTermList .term-btn').length; i++){
    $("#termFormID_"+i).on("click", function() {
      clickTerm($(this))
    });
  };
  $("#submitButton").on("click", function() {
    submitTerm();
  });
});

function clickTerm(term){
  $(".term-btn").removeClass("active");
  term.addClass('active');
}

function submitRequest(method,identifier){
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

function submitTerm(){
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

function displayProgramInfo(){
  var programInfo = $("#programSelect option:selected")[0]
  $("#emailReplyTo").val($(programInfo).data("replytoemail"))
  $("#emailSenderName").val($(programInfo).data("sendername"))

}