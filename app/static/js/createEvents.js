
function toggleEndDate(){
  if ($('input[name="recurringEvent"]:checked').val() == "true"){
    $(".endDates").removeClass("d-none");
  }else{
    $(".endDates").addClass("d-none");
  }

}

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

function createDict(){
  var eventName = $("#inputEventName").val();
  var term = $("#inputEventTerm").find("option:selected").attr("value");
  var recurringEvents= $('input[name="recurringEvent"]:checked').val();
  var startDate = $("#pickStartDate").val();
  var endDate = $("#pickEndDate").val();
  var startTime = $("#pickStartTime").val();
  var endTime = $("#pickEndTime").val();
  var location = $("#inputEventLocation").val();
  var requiredForProgram = $("#checkIsRequired").is(":checked");
  var requireForRSVP = $("#rsvp").is(":checked");
  var serviceHours = $("#earnServiceHours").is(":checked");
  var description = $("#inputEventDescription").val();
  var facilitators = $("#inputEventFacilitators").val();

  var eventDict = {evName: eventName,
                   evTerm: term,
                   evRecurringEvent: recurringEvents,
                   evStartDate: startDate,
                   evEndDate: endDate,
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
  console.log(data)
  $.ajax({
   method: "POST",
   url: '/createEvents',
   contentType: "application/html",
   dataType: "json",
   data: data,
   success: function(result) {
     alert(result)
     console.log(result)
   },
   error: function(result, error){
     alert(error)
     console.log(error)
   }
  });
}
