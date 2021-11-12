$(document).ready(function() {
  $(".form-check-input").click(function updateInterest(el){
    console.log("passed");
    var programID = $(this).attr('id');
    var interest = $(this).is(':checked');

    if (interest) {
      var routeUrl = "/addInterest/"
    }
    else {
      var routeUrl = "/deleteInterest/"
    }

    $.ajax({
      method: "POST",
      url: routeUrl + programID,
      success: function(response) {
          msgFlash("Your interest has been updated", "success")
      },
      error: function(request, status, error) {
        console.log(status,error);
        msgFlash("Error Updating Interest", "danger")
        window.location.reload(true);
      }
    });
  });
});


// onchange="updateBackgroundCheck(1)"
function updateBackgroundCheck(setTo){
  console.log(" This is a test")
  let data = {
      setTo : setTo,
      user: "khatts"
  }

  $.ajax({
    url: "/updateBackgroundCheck",
    type: "POST",
    data: data,
    success: function(s){
        location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }

  })
}
