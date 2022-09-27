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

  // set up sortable requirements list
    $(".frequency-select").change(function () {
        if(!$(this).val()) {
            $(this).addClass("empty");
        } else {
            $(this).removeClass("empty");
        }
    });
    $(".frequency-select").change();
});

function submitRequest(year, method, username){
  $.ajax({
    url: `/bonner/${year}/${method}/${username}`,
    type: "POST",
    success: function(s){
        reloadWithAccordion("cohort-" + year)
    },
    error: function(error, status){
      console.log(error, status)
    }
  })
}
