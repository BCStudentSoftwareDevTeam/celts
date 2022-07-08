import searchUser from './searchUser.js'
function callback(selected) {
  $("#searchStudentsInput").val(selected["username"])
  $("#searchStudent").submit();
}

$("#searchStudentsInput").on("input", function() {
  searchUser("searchStudentsInput", callback);
});
