

function getEventName() {
    var name = document.getElementById("inputEventName").value;
    // nameValue.value = nameValue.value.toUpperCase();
    return name
}

function getEventTerm(){
  var term = document.getElementById("inputEventTerm").value;
  return term
}

function isRecurringEvent(){
  document.getElementsByName("recurringEvent")
    .forEach(radio => {
      if (radio.checked){
        console.log(radio.value);
      }
    });
}

// function isNotRecurringEvent(){
//   var recurringEvent = document.getElementById("no").value;
//   console.log(recurringEvent);
//   return recurringEvent
// }

function getEventLocation() {
    var location = document.getElementById("inputEventLocation").value;
    return location
}

function getEventDescription() {
    var description = document.getElementById("inputEventDescription").value;
    return description
}
function getEventFacilitators() {
    var facilitators = document.getElementById("inputEventFacilitators").value;
    return facilitators
}
