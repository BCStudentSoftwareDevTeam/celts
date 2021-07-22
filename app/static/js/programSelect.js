
function setCurrentOption(el){

  $("#programSubmit").prop("disabled", false)
  $(".active").attr("class", "list-group-item list-group-item-action")
  $(el).attr('class', 'list-group-item list-group-item-action active')
  programChoice = $(".active").attr("id")
  $("#programChoice").attr('value', programChoice)
}
