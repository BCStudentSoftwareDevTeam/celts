import searchUser from './searchUser.js'

function callback() {
  $("#searchStudent").submit();
}

$("#searchStudentsInput").on("input", function(e) {
  searchUser("searchStudentsInput", callback);
});
