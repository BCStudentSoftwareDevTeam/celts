import searchUser from './searchUser.js'

function callback() {
  $("#searchStudent").submit();
}

$("#searchStudentsInput").on("input", function() {
  console.log("The function is called");
  searchUser("searchStudentsInput", callback);
});
