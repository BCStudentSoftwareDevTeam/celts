import searchUser from './searchUser.js'
function callback(selected) {
  $("#searchStudent").submit();
}
$(document).ready(function() {
  $("#searchStudentsInput").on("input", function() {
    searchUser("searchStudentsInput", callback);
  });
  
  $("#searchIcon").click(function (e) {
    e.preventDefault();
    callback($("#searchStudentsInput").val());
  });
  $("#searchStudentsInput").focus() 
})

