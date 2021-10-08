function selectTerm(totalTerms, term){
  $("#submitScannerData").val() = term;
  // $("#currentTermList").
};

function submitTerm(){
  termInfo = {id: term}
  $.ajax({
    url: "/changeCurrentTerm",
    type: "POST",
    data: termInfo,
    success: function(s){
        location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }
  })
};
