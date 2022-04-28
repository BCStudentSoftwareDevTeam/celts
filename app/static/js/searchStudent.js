import searchUser from './searchUser.js'

function callback() {
  $("#searchStudent").submit();
}

$("#searchStudentsInput").on("input", function() {
  var searchOptions = {
    inputId:"searchStudentsInput",
    callback:callback,
  }
  searchUser(searchOptions);
});
