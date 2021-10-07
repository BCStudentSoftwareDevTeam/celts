import searchUser from './searchUser.js'

function submitAdmin(){
  console.log("Yes the submit functin  is called");
  data = {
      method : 1,
      user : "khatts",
      from: "ajax"
  }
  $.ajax({
    url: "/manageUsers/<method>/<user>",
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
    submitAdmin()
  });
});
