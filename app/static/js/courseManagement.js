function changeTerm() {
  var termId = $('option:selected', selectTerm).attr('value');
  console.log("lalalalalalal", termId);
  currentRequest = $.ajax({
    type: "POST",
    url: "/courseManagement",
    data: JSON.stringify(termId),
    contentType: "application/json"})
}
