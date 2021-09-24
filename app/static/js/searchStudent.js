import searchUser from './searchUser.js'

$("#searchStudentsInput").on("input", function() {
  searchUser("searchStudentsInput", "searchStudent");
});
