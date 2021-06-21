$(document).ready(function() {
$(".form-check-input").click(function updateInterest(el){
  //create bool var storing interest or no interest
  var programID = $(this).attr('id');
  var interest = $(this).is(':checked');
  var userID = $("#escalerapadronl").attr("id")
  console.log(programID)
  //create ajax call with data
  console.log("Enter Function");
  if (interest) {
    console.log("Enter IF");
  $.ajax({
    method: "POST",
    url: "/addInterest/" + programID + '/' + userID,
    data: programID, userID,
    success: function(response) {
      if (response) {
        $("#flasher-container").prepend('<div class="alert" id="flasher" data-dismiss="alert" role="alert">This is a success alert—check it out!</div>');
        $("#flasher").delay(3000).fadeOut();

      }
    },
    error: function(request, status, error) {
      console.log(request.responseText);
    }
  });
  }
  else{
    console.log("Enter ELSE");
  $.ajax({
    method: "POST",
    url: "/deleteInterest/" + programID + '/' + userID,
    data: programID, userID,
    success: function(response) {
      if (response) {
        $("#flasher-container").prepend('<div class="alert" id="flasher" data-dismiss="alert" role="alert">This is a success alert—check it out!</div>');
        $("#flasher").delay(3000).fadeOut();

      }
    },
    error: function(request, status, error) {
      console.log(request.responseText);
    }
  });
}
});
});
