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

  document.getElementById('submitParticipant').addEventListener('click', function() {
    // Call the function storingMultipleOfferingEventAttributes() when the button is clicked
    storingMultipleOfferingEventAttributes();
    $("#checkIsMultipleOffering").prop('checked', true);
    // Remove the modal and overlay from the DOM
    $('#modalMultipleOffering').modal('hide');
});

function storingMultipleOfferingEventAttributes() {
    let entries = [];
    $(".extraSlots").children().each(function(index, element) {
        let rowData = $.map($(element).find("input"), (el) => $(el).val());
        console.log("Data in row " + (index + 1) + ": " + rowData);

        entries.push({
            eventName: rowData[0],
            eventDate: rowData[1],
            startTime: rowData[2],
            endTime: rowData[3]
        });
    });

    let entriesJson = JSON.stringify(entries);
    document.getElementById("multipleOfferingDataId").value = entriesJson

  var multipleOfferingTable = $("#multipleOfferingEventsTable");
  multipleOfferingTable.find("tbody tr").remove(); // Clear existing rows
  entries.forEach(function(entry){
    //fromat to 12hr time for display
    var startTime = format24to12HourTime(entry.startTime);
    var endTime = format24to12HourTime(entry.endTime);
    multipleOfferingTable.append("<tr><td>" + entry.eventName + "</td><td>" + entry.eventDate +"</td><td>" + startTime + "</td><td>" + endTime + "</td></tr>");
  });
}  

/*
 * Run when the webpage is ready for javascript
 */
$(document).ready(function() {
  if ( $(".startDatePicker")[0].value != $(".endDatePicker")[0].value){
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

  $("#checkIsRecurring, #checkIsMultipleOffering").click(function() { //#checkIsRecurring, #checkIsMultipleOffering are attributes for the toggle buttons on create event page  createEvent.html line 157-160
    var recurringStatus = $("input[id='checkIsRecurring']:checked").val(); //this line function is to retrive ON when its toggle for recurring event on createEvent.html line 158
    var multipeOfferingStatus = $("input[id='checkIsMultipleOffering']:checked").val();// this line function is to retrive ON when toggle for multiple offering event button createEvent.html line 160
    if (recurringStatus == 'on') {
      $(".endDateStyle, #recurringTableDiv").removeClass('d-none');// this line removes the display none button of bootstrap so that the end-date div appears for recurring event
      $(".endDatePicker").prop('required', true);
    } else {
      $(".endDateStyle, #recurringTableDiv").addClass('d-none');
      $(".endDatePicker").prop('required', false);
    }
    if (multipeOfferingStatus == 'on') {
      $('#modalMultipleOffering').modal('show');// this line pop up the modal for the multiple offering event
      $('#nonMultipleOfferingTime, #nonMultipleOfferingDate').addClass('d-none'); // this line disappear the non multiple offering time and dates and replace them with recurring table div for multiple offering events to show
      $("#multipleOfferingTableDiv").removeClass('d-none');
      $("#checkIsMultipleOffering").prop('checked', true);
    }
    else if (multipeOfferingStatus == undefined){
      $("#multipleOfferingTableDiv").addClass('d-none');
      $('#modalMultipleOffering').modal('hide');
    }
  });
  
  $(".btn-close, #cancelModalPreview").click(function(){ //this function is to untoggle the button when the modal has cancel or close button being clicked
    $("#checkIsMultipleOffering").prop('checked', false);
    $('#nonMultipleOfferingTime, #nonMultiplOfferingDate').removeClass('d-none');
    $("#multipleOfferingTableDiv").addClass('d-none');
    $('#modalMultipleOffering').modal('hide');
    $('.extraSlots').children().not(':first').remove();
    //$('.extraSlots').empty();//this line remove the added multiple offering event slots from appearing if the multiple offering modal is toggle again
  });
  
  /*cloning the div with ID multipleOfferingEvent and cloning, changing the ID of each clone going up by 1. This also changes the ID of the deleteMultipleOfferingEvent so that when the trash icon is clicked, 
  that specific row will be deleted*/
  let counterAdd = 0 // counter to add customized ids into the newly created slots
  $(".addMultipleOfferingEvent").click(function(){
    counterAdd += 1
    let clonedMultipleOffering = $("#multipleOfferingEvent").clone();// this line clones the multipleOfferingEvent id div in the multiple offering event modal on createEvent.html line 403
    clonedMultipleOffering.attr("id", "multipleOfferingEvent" + counterAdd)
    clonedMultipleOffering.find("#deleteMultipleOfferingEvent").attr("id", "deleteMultipleOfferingEvent" + counterAdd).removeClass('d-none');
    $(".extraSlots").append(clonedMultipleOffering)

    //this is so that the trash icon can be used to delete the event
    clonedMultipleOffering.on("click", "[id^=deleteMultipleOfferingEvent]", function() {
      var id = $(this).attr('id').match(/\d+/)[0]; // Extract the numeric part from the id
      $("#multipleOfferingEvent" + id).remove(); 
    });
  });

  $("#allowPastStart").click(function() {
    var allowPast = $("#allowPastStart:checked").val()
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

  $.datepicker.setDefaults({
    minDate:  new Date($.now()),
    dateFormat:'mm-dd-yy'
  });

  $(".startDate").click(function() {
    $("#startDatePicker-" + $(this).data("page-location")).datepicker().datepicker("show");
  });

  $(".endDate").click(function () {
    $("#endDatePicker-" + $(this).data("page-location")).datepicker("show");
  });

  $(".endDate").click(function() {
    $("#endDatePicker-" + $(this).data("page-location")).datepicker().datepicker("show");
  });

  $(".startDatePicker, .endDatePicker").change(function(){
    if ( $(this).val() && $("#endDatePicker-" + $(this).data("page-location")).val()){
      calculateRecurringEventFrequency();
    }
  });

  // $(".multipleOfferingDate").click(function() {
  //   $(#multipleOfferingDatePicker-" + $(this).data("page-location")).datepicker().datepicker("show");
  // });

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

  $(".startDatePicker").change(function(){
     updateDate(this)
  });

//   $(".multipleOfferingDatePicker").change(function(){ //multiple offering data calender function
//     updateDate(this)
//  });

  $("#inputCharacters").keyup(function (event) {
    setCharacterLimit(this, "#remainingCharacters");
  });

  setCharacterLimit($("#inputCharacters"), "#remainingCharacters");
});
