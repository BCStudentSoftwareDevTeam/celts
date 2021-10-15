import searchUser from './searchUser.js'

function callback() {
  console.log("This function is called")
  $("#searchAdmin").submit();
}

$(document).ready(function() {
  // add celts admin
  $("#searchCeltsAdminInput").on("input", function() {
    searchUser("searchCeltsAdminInput", callback);
  });

  $("#addCeltsAdmin").on("click", function() {
    submitRequest("addCeltsAdmin","#searchCeltsAdminInput")
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

  for (i=1; i<=parseInt($('#totalTerms').val()); i++){
    $("#termFormID_"+i).on("click", function() {
      console.log($(this).val())
      clickTerm($('#totalTerms').val(), $(this).val())
    });
  }

});


function submitRequest(method,identifier){
  let data = {
      method : method,
      user : $(identifier).val(),
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

function clickTerm(totalTerms, term){
  $("#termInput").val(term);
  for (i=1; i<=totalTerms; i++){
    if ($('#termFormID_' + i).hasClass('active')){
     $('#termFormID_' + i).removeClass('active');
    }
  }
  $('#termFormID_' + term).addClass('active');
};

function submitTerm(){
  termInfo = {id: $("#termInput").val()}
  $.ajax({
    url: "/changeCurrentTerm",
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
