import searchUser from './searchUser.js'

function callback(selected) {
  $("#searchStudentsInput").closest("form").submit();
}

$(document).ready(function() {
  searchUser("searchStudentsInput", callback);   // initialize ONCE

  $("#searchIcon").click(function (e) {
    e.preventDefault();
    callback($("#searchStudentsInput").val());
  });

  $("#searchStudentsInput").focus();
});