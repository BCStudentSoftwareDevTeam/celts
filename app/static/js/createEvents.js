//import createEvents from 'app/controllers/admin/createEvents.py';
//{% from 'app.controllers.admin.createEvents' import createEvents %}

// function getEventName() {
//   var name = document.getElementById("inputEventName").value;
//   // nameValue.value = nameValue.value.toUpperCase();
//   return name
// }

// function getEventTerm(){
//   var term = document.getElementById("inputEventTerm").value;
//   return term
// }

// function isRecurringEvent(){
//   var recurringEvent
//   document.getElementsByName("recurringEvent")
//     .forEach(radio => {
//       if (radio.checked){
//         recurringEvent= radio.value;
//       }
//     });
//   if (recurringEvent == "true"){
//     recurringEvent = true;
//   }else{
//     recurringEvent = false;
//   }
//   return recurringEvent;
// }

// function getStartDate(){
//   var startDate = document.getElementById("pickStartDate").value;
//   console.log(startDate)
//   return startDate
// }

// function getStartTime(){
//   var startTime = document.getElementById("pickStartTime").value;
//   console.log(startTime)
//   return startTime
// }

// function getEndTime(){
//   var endTime = document.getElementById("pickEndTime").value;
//   console.log(endTime)
//   return endTime
// }
// function getEventLocation() {
//     var location = document.getElementById("inputEventLocation").value;
//     return location
// }

// function getIsRequiredForProgram() {
//   var requiredForProgram = document.getElementById("checkIsRequired").checked;
//   return requiredForProgram
// }

// function getRequireForRSVP(){
//   var requireForRSVP = document.getElementById("rsvp").checked;
//   return requireForRSVP
// }

// function getEarnServiceHours(){
//   var serviceHours = document.getElementById("earnServiceHours").checked;
//   return serviceHours
// }
//
// function getEventDescription() {
//     var description = document.getElementById("inputEventDescription").value;
//     return description
// }
//
// function getEventFacilitators() {
//     var facilitators = document.getElementById("inputEventFacilitators").value;
//     return facilitators
// }

function dropHandler(ev) {
  console.log('File(s) dropped');
  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();

  if (ev.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    for (var i = 0; i < ev.dataTransfer.items.length; i++) {
      // If dropped items aren't files, reject them
      if (ev.dataTransfer.items[i].kind === 'file') {
        var file = ev.dataTransfer.items[i].getAsFile();
        console.log('... file[' + i + '].name = ' + file.name);
      }
    }
  } else {
    // Use DataTransfer interface to access the file(s)
    for (var i = 0; i < ev.dataTransfer.files.length; i++) {
      console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
    }
  }
  return file
}
function dragOverHandler(ev) {
  console.log('File(s) in drop zone');

  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
}

function createNewEvent(){
  createEvents()
}
function createDict(){
  var eventName = $("#inputEventName").val();
  var term = $("#inputEventTerm").find("option:selected").attr("value");
  var recurringEvents= $('input[name="recurringEvent"]:checked').val();
  var startDate = $("#pickStartDate").val();
  var startTime = $("#pickStartTime").val();
  var endTime = $("#pickEndTime").val();
  var location = $("#inputEventLocation").val();
  var requiredForProgram = $("#checkIsRequired").is(":checked");
  var requireForRSVP = $("#rsvp").is(":checked");
  var serviceHours = $("#earnServiceHours").is("checked");
  var description = $("#inputEventDescription").val();
  var facilitators = $("#inputEventFacilitators").val();

  var eventDict = {evName: eventName,
                   evterm: term,
                   evRecurringEvent: recurringEvents,
                   evStartDate: startDate,
                   evStartTime: startTime,
                   evEndTime: endTime,
                   evLocation: location,
                   evRequiredForProgram: requiredForProgram,
                   evRSVP: requireForRSVP,
                   evServiceHours: serviceHours,
                   evDescription: description,
                   evFacilitators: facilitators
  }

  return eventDict;


}
function createNewEvent(){
  events = createDict()
  var data = JSON.stringify(events);

  $.ajax({
   method: "POST",
   url: '/createEvents',
   data: data,
   dataType: "json",
   contentType: "application/json",
   success: function(response) {
     alert("Something in progress")
   }

}
