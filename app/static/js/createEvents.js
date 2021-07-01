
// function toggleEndDate(){
//   if ($('input[name="recurringEvent"]:checked').val() == "true"){
//     $("#endDateStyle").removeClass("d-none");
//   }else{
//     $("#endDateStyle").addClass("d-none");
//   }
// }

$(document).ready(function(){

  $(".readonly").on('keydown paste', function(e){ //makes the input fields act like readonly (readonly doesn't work with required)
        if(e.keyCode != 9) // ignore tab
            e.preventDefault();
    });

  $.datepicker.setDefaults({
    dateFormat:'yy-mm-dd'
  });

  $("#calendarIconStart").click(function() {
    $("#startDatePicker").datepicker().datepicker("show"); // Shows the start date datepicker when glyphicon is clicked
  });

  $("#calendarIconEnd").click(function() {
      $("#endDatePicker").datepicker().datepicker("show"); // Shows the start date datepicker when glyphicon is clicked
    });
});

function updateDate(obj) { // updates max and min dates of the datepickers as the other datepicker changes
  var dateToChange = new Date($(obj).val());
  var newMonth = dateToChange.getMonth();
  var newYear = dateToChange.getFullYear();
  if(obj.id == "endDatePicker"){
    var newDay = dateToChange.getDate() + 1;
    $("#startDatePicker").datepicker({maxDate: new Date(newYear, newMonth, newDay)});
    $("#startDatePicker").datepicker("option", "maxDate", new Date(newYear, newMonth, newDay));
  }
  if(obj.id == "startDatePicker"){
    var newDay = dateToChange.getDate() + 1;
    $("#endDatePicker").datepicker({minDate: new Date(newYear, newMonth, newDay)});
    $("#endDatePicker").datepicker( "option", "minDate", new Date(newYear, newMonth, newDay));
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


// function createEventValuesDict(){
//   var eventName = $("#inputEventName").val();
//   var term = $("#inputEventTerm").find("option:selected").attr("value");
//   var recurringEvents= $('input[name="recurringEvent"]:checked').val();
//   var startDate = $("#startDatePicker").datepicker("option", "dateFormat", "yy-mm-dd" ).val();
//   var endDate =  $("#endDatePicker").datepicker("option", "dateFormat", "yy-mm-dd" ).val();
//   var startTime = $("#pickStartTime").val();
//   var endTime = $("#pickEndTime").val();
//   var location = $("#inputEventLocation").val();
//   var requiredForProgram = $("#checkIsRequired").is(":checked");
//   var requireForRSVP = $("#rsvp").is(":checked");
//   var serviceHours = $("#earnServiceHours").is(":checked");
//   var description = $("#inputEventDescription").val();
//   var facilitators = $("#inputEventFacilitators").val();
//
//   var eventDict = {evName: eventName,
//                    evTerm: term,
//                    evRecurringEvent: recurringEvents,
//                    evStartDate: startDate,
//                    evEndDate: endDate,
//                    evStartTime: startTime,
//                    evEndTime: endTime,
//                    evLocation: location,
//                    evRequiredForProgram: requiredForProgram,
//                    evRSVP: requireForRSVP,
//                    evServiceHours: serviceHours,
//                    evDescription: description,
//                    evFacilitators: facilitators
//   }
//   return eventDict;
// }



// function createNewEvent(){
//
//
//       events = createEventValuesDict()
//       var data = JSON.stringify(events);
//       console.log(data)
//       $.ajax({
//        method: "POST",
//        url: '/createEvents',
//        contentType: "application/json",
//        dataType: "text",
//        data: data,
//        success: function(result) {
//          alert(result)
//          console.log(result)
//        },
//        error: function(xhr, status, error){
//          alert("Something went wrong! " + String(error));
//          console.log("Something went wrong!")
//        }
//       });
//
// }
