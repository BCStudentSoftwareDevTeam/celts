import searchUser from './searchUser.js'

function callback() {
  $("#searchStudent").submit();
  console.log("Here");
}

$("#searchStudentsInput").on("input", function() {
  searchUser("searchStudentsInput", callback);
});
