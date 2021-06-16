function updateInterest(el){
  //create bool var storing interest or no interest
  var interest = $(el).is(':checked');
  numInterest = Number(interest) //changed interest to a number because JS booleans and Python Booleans are cased differently but 1 and 0 work the same for both
  //create var with program id
  var programID = $(el).attr('id');
  //create ajax call with data
  $.ajax({
    method: "POST",
    url: "/updateInterest/" + programID + '/' + numInterest,
    data: programID, numInterest,
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
