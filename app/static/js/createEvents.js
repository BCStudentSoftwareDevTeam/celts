import searchUser from './searchUser.js';

// updates max and min dates of the datepickers as the other datepicker changes
function updateDate(obj) {
  var selectedDate = $(obj).datepicker("getDate"); // No need for / for Firefox compatiblity 
  var newMonth = selectedDate.getMonth();
  var newYear = selectedDate.getFullYear();
  var newDay = selectedDate.getDate();

  if (obj.className.includes("startDatePicker")) {
    $("#endDatePicker-" + $(obj).data("page-location")).datepicker("option", "minDate", new Date(newYear, newMonth, newDay));
  } else if (obj.className.includes("endDatePicker")) {
    $("#startDatePicker-" + $(obj).data("page-location")).datepicker("option", "maxDate", new Date(newYear, newMonth, newDay));
  }

  if (obj.className.includes("endDatePicker")) {
    $("#startDatePicker-"+$(obj).data("page-location")).datepicker({maxDate: new Date(newYear, newMonth, newDay)});
    $("#startDatePicker-"+$(obj).data("page-location")).datepicker("option", "maxDate", new Date(newYear, newMonth, newDay));
  }
}


// turns a string with a time with HH:mm format to %I:%M %p format
// used to display 12 hour format but still use 24 hour format in the backend
function format24to12HourTime(timeStr) {
  var formattedTime;
  if (parseInt(timeStr.slice(0, 2)) > 12) {
    formattedTime = "0" + String(parseInt(timeStr.slice(0, 2)) - 12) + timeStr.slice(2) + " PM";
  } else if (parseInt(timeStr.slice(0, 2)) < 12) {
    formattedTime = timeStr + " AM";
  } else {
    formattedTime = timeStr + " PM";
  }
  return formattedTime;
}

function calculateRecurringEventFrequency(){
      var eventDatesAndName = {name:$("#inputEventName").val(),
                               isRecurring: true,
                               startDate:$(".startDatePicker")[0].value,
                               endDate:$(".endDatePicker")[0].value}
      $.ajax({
        type:"POST",
        url: "/makeRecurringEvents",
        data: eventDatesAndName, //get the startDate, endDate and name as a dictionary
        success: function(jsonData){
          var recurringEvents = JSON.parse(jsonData)
          var recurringTable = $("#recurringEventsTable")
          $("#recurringEventsTable tbody tr").remove();
          for (var event of recurringEvents){
            var eventdate = new Date(event.date).toLocaleDateString()
            recurringTable.append("<tr><td>"+event.name+"</td><td><input name='week"+event.week+"' type='hidden' value='"+eventdate+"'>"+eventdate+"</td></tr>");
            }
        },
        error: function(error){
          console.log(error)
        }
      });
  }
  
$(document).ready(function () {
  // Initialize datepicker with proper options
  $.datepicker.setDefaults({
    dateFormat: 'yy/mm/dd', // Ensures compatibility across browsers
    minDate: new Date()
  });

  $(".datePicker").datepicker({
    dateFormat: 'mm/dd/yy',
    minDate: new Date() 
  });

    $(".datePicker").each(function() {
    var dateStr = $(this).val();
    if (dateStr) {
      var dateObj = new Date(dateStr);
      if (!isNaN(dateObj.getTime())) {
        $(this).datepicker("setDate", dateObj);
      }
    }
  });

  // Update datepicker min and max dates on change
  $(".startDatePicker, .endDatePicker").change(function () {
    updateDate(this);
  });

  if ($(".startDatePicker")[0].value != $(".endDatePicker")[0].value) {
    calculateRecurringEventFrequency();
  }

  handleFileSelection("attachmentObject");

  $("#checkRSVP").on("click", function () {
    if ($("#checkRSVP").is(":checked")) {
      $("#limitGroup").show();
    } else {
      $("#limitGroup").hide();
    }
  });

  // Disable button when we are ready to submit
  $("#saveEvent").on('submit', function (event) {
    $(this).find("input[type=submit]").prop("disabled", true);
  });

<<<<<<< HEAD
  $("#checkIsRecurring").click(function () {
    var recurringStatus = $("input[name='isRecurring']:checked").val();
=======
  $("#checkIsRecurring, #checkIsCustom").click(function() {
    var recurringStatus = $("input[id='checkIsRecurring']:checked").val()
    var customStatus = $("input[id='checkIsCustom']:checked").val()
    console.log(recurringStatus +"recurring")
>>>>>>> 81724e36 (modal toggle button created)
    if (recurringStatus == 'on') {
      $(".endDateStyle, #recurringTableDiv").removeClass('d-none');
      $(".endDatePicker").prop('required', true);
<<<<<<< HEAD
    } else {
      $(".endDateStyle, #recurringTableDiv").addClass('d-none');
=======
    } 
    else if (recurringStatus == undefined){
      $(".endDateStyle, #recurringTableDiv").addClass('d-none')
>>>>>>> 81724e36 (modal toggle button created)
      $(".endDatePicker").prop('required', false);
    }
    if (customStatus == 'on') {
      $(".modalCustomEvent").removeClass('d-none')
    } 
    else if (customStatus == undefined){
      $(".modalCustomEvent").addClass('d-none')
    }
  });
<<<<<<< HEAD

  $("#allowPastStart").click(function () {
    var allowPast = $("#allowPastStart:checked").val();
=======
  
  
  $("#allowPastStart").click(function() {
    var allowPast = $("#allowPastStart:checked").val()
>>>>>>> 81724e36 (modal toggle button created)
    if (allowPast == 'on') {
      $.datepicker.setDefaults({
        minDate: new Date('1999/10/25'),
        dateFormat: 'yy-mm-dd' // Ensures compatibility across browsers
      });
    } else {
      $.datepicker.setDefaults({
        minDate: new Date(),
        dateFormat: 'yy/mm/dd' // Ensures compatibility across browsers
      });
    }
  });

  // everything except Chrome
  if (navigator.userAgent.indexOf("Chrome") == -1) {
    $('input.timepicker').timepicker({
      timeFormat: 'hh:mm p',
      scrollbar: true,
      dropdown: true,
      dynamic: true,
      minTime: "08:00am",
      maxTime: "10:00pm"
    });
    $(".timepicker").prop("type", "text");
    $(".timeIcons").prop("hidden", false);

    var formattedStartTime = format24to12HourTime($(".startTime").prop("defaultValue"));
    var formattedEndTime = format24to12HourTime($(".endTime").prop("defaultValue"));
    $(".startTime").val(formattedStartTime);
    $(".endTime").val(formattedEndTime);
  } else {
    $(".timepicker").prop("type", "time");
    $(".timeIcons").prop("hidden", true);
  }

  if ($(".datePicker").is("readonly")) {
    $(".datePicker").datepicker("option", "disabled", true);
  }

  $(".readonly").on('keydown paste', function (e) {
    if (e.keyCode != 9) // ignore tab
      e.preventDefault();
  });

  $(".startDate").click(function () {
    $("#startDatePicker-" + $(this).data("page-location")).datepicker("show");
  });

  $(".endDate").click(function () {
    $("#endDatePicker-" + $(this).data("page-location")).datepicker("show");
  });

  $(".startDatePicker, .endDatePicker").change(function () {
    if ($(this).val() && $("#endDatePicker-" + $(this).data("page-location")).val()) {
      calculateRecurringEventFrequency();
    }
  });

  $("#checkRSVP").click(function () {
    if ($("input[name='isRsvpRequired']:checked").val() == 'on') {
      $("#checkFood").prop('checked', true);
    } else {
      $("#checkFood").prop('disabled', false);
    }
  });

  var facilitatorArray = [];
  function callback(selectedFacilitator) {
    let facilitator = (selectedFacilitator["firstName"] + " " + selectedFacilitator["lastName"] + " (" + selectedFacilitator["username"] + ")");
    let username = selectedFacilitator["username"];
    if (!facilitatorArray.includes(username)) {
      facilitatorArray.push(username);
      let tableBody = $("#facilitatorTable").find("tbody");
      let lastRow = tableBody.find("tr:last");
      let newRow = lastRow.clone();
      newRow.find("td:eq(0) p").text(facilitator);
      newRow.find("td:eq(0) div button").data("id", username);
      newRow.find("td:eq(0) div input").attr("id", username);
      newRow.attr("id", username);
      newRow.prop("hidden", false);
      lastRow.after(newRow);
      $("#hiddenFacilitatorArray").attr("value", facilitatorArray);
    }
  }

  $("#eventFacilitator").on('input', function () {
    searchUser("eventFacilitator", callback, true, undefined, "instructor");
  });

  $("#facilitatorTable").on("click", "#remove", function () {
    let username = $(this).closest("tr")[0].id;
    const index = facilitatorArray.indexOf(username);
    facilitatorArray.splice(index, 1);
    $("#hiddenFacilitatorArray").attr("value", facilitatorArray);
    $(this).closest("tr").remove();
  });

  $(".endDatePicker").change(function () {
    updateDate(this);
  });

  $(".startDatePicker").change(function () {
    updateDate(this);
  });

  $("#inputCharacters").keyup(function (event) {
    setCharacterLimit(this, "#remainingCharacters");
  });

  setCharacterLimit($("#inputCharacters"), "#remainingCharacters");
});
