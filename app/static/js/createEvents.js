
function toggleEndDate(){
  if ($('input[name="recurringEvent"]:checked').val() == "true"){
    $("#endDateStyle").removeClass("d-none");
  }else{
    $("#endDateStyle").addClass("d-none");
  }
}

$(document).ready(function(){

  $("#calendarIconStart").click(function() {
    $("#startDatePicker").datepicker().datepicker("show"); // Shows the start date datepicker when glyphicon is clicked
  });

  $("#calendarIconEnd").click(function() {
      $("#endDatePicker").datepicker().datepicker("show"); // Shows the start date datepicker when glyphicon is clicked
    });

    $("#pickStartTime").click(function() {
      $('#pickStartTime').timepicker().focus();
    });


    $("#pickEndTime").click(function() {
      $('#pickEndTime').timepicker().focus();
    });
      });




function fillDates(response) { // prefill term start and term end
  $("#primary-cutoff-warning").hide();
  $("#break-cutoff-warning").hide();
  $("#primary-cutoff-date").text("");
  $("#addMoreStudent").show();

  $("#selectedTerm").on("change", function(){
    $("#jobType").val('');
  });
  for (var key in response){
    var start = response[key]["Start Date"];
    var end = response[key]["End Date"];
    var primaryCutOff = response[key]["Primary Cut Off"];
    // disabling primary position if cut off date is before today's date
    var today = new Date();
    var date = ("0"+(today.getMonth()+1)).slice(-2)+"/"+("0"+today.getDate()).slice(-2)+"/"+today.getFullYear();
    var isBreak = response[key]["isBreak"];
    var isSummer = response[key]["isSummer"];
    if (primaryCutOff){
      if (isBreak){
        if (Date.parse(date) > Date.parse(primaryCutOff)){
        msgFlash("The deadline to add break positions has ended.", "fail");
        $("#break-cutoff-warning").show();
        $("#break-cutoff-date").text(primaryCutOff);
        $("#addMoreStudent").hide();
        }
      }
      else{
        if (Date.parse(date) > Date.parse(primaryCutOff)){
          $("#jobType option[value='Primary']").attr("disabled", true );
          $('.selectpicker').selectpicker('refresh');
          msgFlash("Disabling primary position because cut off date is before today's date", "fail");
          $("#primary-cutoff-warning").show();
          $("#primary-cutoff-date").text(primaryCutOff);
        }
        else{
          $("#jobType option[value='Primary']").attr("disabled", false );
          $('.selectpicker').selectpicker('refresh');
        }
      }

    }
    // Start Date
    var startd = new Date(start);
    var dayStart1 = startd.getDate();
    var monthStart1 = startd.getMonth();
    var yearStart = startd.getFullYear();
    // End Date
    var endd = new Date(end);
    var dayEnd1 = endd.getDate();
    var monthEnd1 = endd.getMonth();
    var yearEnd = endd.getFullYear();
    // Pre-populate values
    $("#").val(start);
    $("#endDatePicker").val(end);
    $("#startDatePicker").datepicker("option", "minDate", new Date(yearStart, monthStart1, dayStart1));
    $("#startDatePicker").datepicker("option", "maxDate", new Date(yearEnd, monthEnd1, dayEnd1));
    $("#endDatePicker").datepicker("option", "maxDate", new Date(yearEnd, monthEnd1, dayEnd1));
    $("#endDatePicker").datepicker("option", "minDate", new Date(yearStart, monthStart1, dayStart1));
    $("#startDatePicker").datepicker({
      beforeShowDay: function(d) {

        if(d.getTime() < startd.getTime()){
          return [false, 'datePicker', 'Before Term Start'];
        }
        else if (d.getTime() > endd.getTime()) {
          return [false, 'datePicker', 'After Term End'];
        }else{
            return [true, '', 'Available'];
        }
    },
  });
    $("#endDatePicker").datepicker({
    beforeShowDay: function(d) {

        if(d.getTime() > endd.getTime()){
          return [false, 'datePicker', 'After Term End'];
        }
        else if (d.getTime() < startd.getTime()) {
          return [false, 'datePicker', 'Before Term Start'];
        }else{
            return [true, '', 'Available'];
        }
    },
    });
  }
}

function updateDate(obj) { // updates max and min dates of the datepickers as the other datepicker changes
  var dateToChange = new Date($(obj).val());
  var newMonth = dateToChange.getMonth();
  var newYear = dateToChange.getFullYear();
  if(obj.id == "endDatePicker"){
    var newDay = dateToChange.getDate() - 1;
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

function createDict(){
  var eventName = $("#inputEventName").val();
  var term = $("#inputEventTerm").find("option:selected").attr("value");
  var recurringEvents= $('input[name="recurringEvent"]:checked').val();
  var startDate = $("#startDatePicker").datepicker("option", "dateFormat", "yy-mm-dd" ).val();
  var endDate =  $("#endDatePicker").datepicker("option", "dateFormat", "yy-mm-dd" ).val();
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
   contentType: "application/json",
   dataType: "text",
   data: data,
   success: function(result) {
     alert(result)
     console.log(result)
   },
   error: function(xhr, status, error){
     alert("Something went wrong!");
     console.log("Something went wrong!")
   }
  });
}
