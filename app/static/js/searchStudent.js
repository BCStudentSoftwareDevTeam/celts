import searchUser from './searchUser.js'

function callback() {
  $("#searchStudent").submit();
}

$("#searchStudentsInput").on("keydown", function(this) {
    if($("#searchStudentsInput").val() == '')
      return event.key != "Enter";
});

$("#searchStudentsInput").on("input", function(e) {
  searchUser("searchStudentsInput", callback);
});
