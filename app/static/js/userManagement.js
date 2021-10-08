import searchUser from './searchUser.js'




function callback() {
  console.log("This function is called")
  $("#searchAdmin").submit();
}

$(document).ready(function() {
  $("#searchCeltsAdminInput").on("input", function() {
    console.log("This is reached.");
    searchUser("searchCeltsAdminInput", callback);
  });

  $("#addCeltsAdmin").on("click", function() {
    submitAdmin("addCeltsAdmin")
  });
});

function submitAdmin(method){
  console.log("Yes the submit functin  is called");
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
