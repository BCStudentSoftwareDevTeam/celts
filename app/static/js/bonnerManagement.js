import searchUser from './searchUser.js'

$(document).ready(function(){
  $("input[type=search]").on("input", function(){
      let year = $(this).data('year')
      searchUser(this.id, s => submitRequest(year, "add", s.username), false, null, "student")
  });
  $(".removeBonner").on("click",function(){
    let year = $(this).data('year')
    submitRequest(year, "remove", $(this).data("username"));
  });
});

function submitRequest(year, method, username){
  $.ajax({
    url: `/bonner/${year}/${method}/${username}`,
    type: "POST",
    success: function(s){
        location.reload()
    },
    error: function(error, status){
      console.log(error, status)
    }
  })
}
