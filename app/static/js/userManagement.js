import searchUser from './searchUser.js'

function callback() {
  console.log("This function is called")
  $("#searchAdmin").submit();
}

$("#searchCeltsAdminInput").on("input", function() {
  console.log("This is reached.");
  searchUser("searchCeltsAdminInput", callback);
});
