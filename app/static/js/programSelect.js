
function programSelected(el){
  programChoice = $(el).attr("id")
  if($(el).prop("checked")){
    $("#programName").append("<input type='hidden' id='programChoice' value='" + programChoice + "'name='programChoice'>")
  }
  else {
    $("#programChoice").remove()
  }
}

function setCurrentOption(el){
  $(el).attr('class', 'list-group-item list-group-item-action active')
}
