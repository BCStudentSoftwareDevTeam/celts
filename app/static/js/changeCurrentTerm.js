function selectTerm(totalTerms, term){
  $("#termInput").val(term);
  for (i=1; i<=totalTerms; i++){
    if ($('#termFormID_' + i).hasClass('active')){
     $('#termFormID_' + i).removeClass('active');
    }
  }
  $('#termFormID_' + term).addClass('active');
};

function submitTerm(){
  termInfo = {id: $("#termInput").val()}
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
