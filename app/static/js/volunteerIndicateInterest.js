function updateInterest(el){
  //create bool var storing interest or no interest
  var interest = $(el).is(':checked');
  //create var with program id
  var programID = $(el).attr('id');
  //create ajax call with data
  $.ajax({
    method: "POST",
    url: "/updateInterest/" + programID + '/' + interest,
    data: programID, interest,
    success: function(response) {
      if (response) {
        console.log('YAY YOU MADE IT BACK');
      }
    }
  });

}
