$(document).ready(function() {
$(".form-check-input").click(function updateInterest(el){
  //create bool var storing interest or no interest
  var interest = $(this).is(':checked');
  var userID = $("#escalerapadronl").attr("id")
  console.log(userID);
  var programID = $(el).attr('id');
  console.log(programID);
  //create ajax call with data
  console.log("Enter Function");
  console.log(interest);
  if (interest) {
    console.log("Enter IF");
  $.ajax({
    method: "POST",
    url: "/addInterest/" + programID + '/' + userID,
    data: programID, userID,
    success: function(response) {
      if (response) {
        //Add flasher to give user feedback that database is updated
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
        //Add flasher to give user feedback that database is updated
      }
    },
    error: function(request, status, error) {
      console.log(request.responseText);
    }
  });
}

});
});
