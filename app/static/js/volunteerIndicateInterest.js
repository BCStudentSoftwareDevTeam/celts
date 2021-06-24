$(document).ready(function() {
$(".form-check-input").click(function updateInterest(el){
  var programID = $(this).attr('id');
  var interest = $(this).is(':checked');
  var userID = $(this).attr("id")
  if (interest) {
    var routeUrl = "/addInterest/"
  }
  else {
    var routeUrl = "/deleteInterest/"
  }
  $.ajax({
    method: "POST",
    url: routeUrl + programID + '/' + userID,
    data: programID, userID,
    success: function(response) {
      if (response) {
        $("#flasher-container").prepend('<div class="alert alert-success"" id="flasher" data-dismiss="alert" role="alert">Your Interest have been Updated</div>');
        $("#flasher").delay(3000).fadeOut();
      }
    },
    error: function(request, status, error) {
      console.log(request.responseText);
    }
  });
  });
  });
