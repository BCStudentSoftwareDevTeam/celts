import searchUser from './searchUser.js'

function callback() {
  $("#searchAdmin").submit();
}

$(document).ready(function() {
  // add celts admin
  $("#searchCeltsAdminInput").on("input", function() {
    var searchOptions = {
      inputId:"searchCeltsAdminInput",
      callback:callback,
    };
    searchUser(searchOptions);
  });

  $("#addCeltsAdmin").on("click", function() {
    submitRequest("addCeltsAdmin","#searchCeltsAdminInput")
  });

  $("#addNewTerm").on("click",function(){
    addNewTerm();
  });
  // add celts student staff
  $("#searchCeltsStudentStaffInput").on("input", function() {
    var searchOptions = {
      inputId:"searchCeltsStudentStaffInput",
      callback:callback,
    };
    searchUser(searchOptions);
  });

  $("#addCeltsStudentStaff").on("click", function() {
    submitRequest("addCeltsStudentStaff","#searchCeltsStudentStaffInput")
  });

  // remove celts admin
  $("#removeCeltsAdminInput").on("input", function() {
    var searchOptions = {
      inputId:"removeCeltsAdminInput",
      callback:callback,
    };
    searchUser(searchOptions);
  });

  $("#removeCeltsAdmin").on("click", function() {
    submitRequest("removeCeltsAdmin","#removeCeltsAdminInput")
  });

  // remove celts student staff
  $("#removeCeltsStudentStaffInput").on("input", function() {
    var searchOptions = {
      inputId:"removeCeltsStudentStaffInput",
      callback:callback,
    };
    searchUser(searchOptions);
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
};

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
};

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
};
