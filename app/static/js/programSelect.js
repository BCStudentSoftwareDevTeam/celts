
function setCurrentOption(el){

  $("#programSubmit").prop("disabled", false)
  $(".active").attr("class", "list-group-item list-group-item-action")
  $(el).attr('class', 'list-group-item list-group-item-action active')
  programChoice = $(".active").attr("id")
  $("#programChoice").attr('value', programChoice)
  activeProgramId = $(".active").attr("name")
  console.log(activeProgramId)
  $("#formSubmit").attr("action", "/" + activeProgramId + "/create_event")
}
