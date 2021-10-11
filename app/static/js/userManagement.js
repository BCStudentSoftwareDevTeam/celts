import searchUser from './searchUser.js'

function callback() {
  console.log("This function is called")
  $("#searchAdmin").submit();
}

$(document).ready(function() {
  // add celts admin
  $("#searchCeltsAdminInput").on("input", function() {
    console.log("This is reached.");
    searchUser("searchCeltsAdminInput", callback);
  });

  $("#addCeltsAdmin").on("click", function() {
    submitAdmin("addCeltsAdmin")
  });

  // add celts student staff
  $("#searchCeltsStudentStaffInput").on("input", function() {
    console.log("This is reached.");
    searchUser("searchCeltsStudentStaffInput", callback);
  });

  $("#addCeltsStudentStaff").on("click", function() {
    submitCeltsStudentStaff("addCeltsStudentStaff")
  });

  // remove celts admin
  $("#removeCeltsAdminInput").on("input", function() {
    console.log("This is reached.");
    searchUser("removeCeltsAdminInput", callback);
  });

  $("#removeCeltsAdmin").on("click", function() {
    submitRemoveCeltsAdmin("removeCeltsAdmin")
  });

  // remove celts student staff
  $("#removeCeltsStudentStaffInput").on("input", function() {
    console.log("This is reached.");
    searchUser("removeCeltsStudentStaffInput", callback);
  });

  $("#removeCeltsStudentStaff").on("click", function() {
    submitRemoveCeltsStudentStaff("removeCeltsStudentStaff")
  });

});

function submitAdmin(method){
  let data = {
      method : method,
      user : $("#searchCeltsAdminInput").val(),
      from: "ajax"
  }
  console.log(data);
  $.ajax({
    url: "/manageUsers",
    type: "POST",
    data: data,
    success: function(s){
        location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }

  })
}

function submitCeltsStudentStaff(method){
  let data = {
      method : method,
      user : $("#searchCeltsStudentStaffInput").val(),
      from: "ajax"
  }
  console.log(data);
  $.ajax({
    url: "/manageUsers",
    type: "POST",
    data: data,
    success: function(s){
        location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }

  })
}

function submitRemoveCeltsAdmin(method){
  let data = {
      method : method,
      user : $("#removeCeltsAdminInput").val(),
      from: "ajax"
  }
  console.log(data);
  $.ajax({
    url: "/manageUsers",
    type: "POST",
    data: data,
    success: function(s){
        location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }

  })
}

function submitRemoveCeltsStudentStaff(method){
  let data = {
      method : method,
      user : $("#removeCeltsStudentStaffInput").val(),
      from: "ajax"
  }
  console.log(data);
  $.ajax({
    url: "/manageUsers",
    type: "POST",
    data: data,
    success: function(s){
        location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }

  })
}
