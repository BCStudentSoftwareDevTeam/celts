import searchUser from './searchUser.js'

function callback(selected) {
  console.log(selected);
  $("#searchStudentsInput").submit();
}

$(document).ready(function() {
  searchUser("searchStudentsInput", callback);   // initialize ONCE

  $("#searchIcon").click(function (e) {
    e.preventDefault();
    callback($("#searchStudentsInput").val());
  });

  $("#searchStudentsInput").focus();
});



// import searchUser from './searchUser.js'
// function callback(selected) {
//   console.log(selected);
//   $("#searchStudentsInput").submit();
// }
// $(document).ready(function() {
//   $("#searchStudentsInput").on("input", function() {    
//     searchUser("searchStudentsInput", callback);
//   });
  
//   $("#searchIcon").click(function (e) {
//     e.preventDefault();
//     callback($("#searchStudentsInput").val());
//   });
//   $("#searchStudentsInput").focus() 
// })

