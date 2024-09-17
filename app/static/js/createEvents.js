import searchUser from './searchUser.js'
let pendingmultipleEvents = []

// updates max and min dates of the datepickers as the other datepicker changes
// No need for / for Firefox compatiblity 
function updateDate(obj) {
  var selectedDate = $(obj).datepicker("getDate"); 
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

function calculateRepeatingEventFrequency(){
      var eventDatesAndName = {name:$("#inputEventName").val(),
                               isRepeating: true,
                               startDate:$(".startDatePicker")[0].value,
                               endDate:$(".endDatePicker")[0].value}
      $.ajax({
        type:"POST",
        url: "/makeRepeatingEvents",
        //get the startDate, endDate and name as a dictionary
        data: eventDatesAndName,
        success: function(jsonData){
          var repeatingEvents = JSON.parse(jsonData)
          var repeatingTable = $("#repeatingEventsTable")
          $("#repeatingEventsTable tbody tr").remove();
          for (var event of repeatingEvents){
            var eventdate = new Date(event.date).toLocaleDateString()
            repeatingTable.append("<tr><td>"+event.name+"</td><td><input name='week"+event.week+"' type='hidden' value='"+eventdate+"'>"+eventdate+"</td></tr>");           
            }
          console.log(repeatingEvents)
        },
        error: function(error){
          console.log(error)
        }
      });
  }
  $('#submitParticipant').on('click', function() {
    //Requires that modal info updated before it can be saved, gives notifier if there are empty fields
    let eventNameInputs = document.querySelectorAll('.multipleOfferingNameField');
    let datePickerInputs = document.querySelectorAll('.multipleOfferingDatePicker');
    let startTimeInputs = document.querySelectorAll('.multipleOfferingStartTime');
    let endTimeInputs = document.querySelectorAll('.multipleOfferingEndTime');
    let isEmpty = false;
    let timeCheck = false;
    eventNameInputs.forEach(eventNameInput => {
      // Check if the input field is empty
      if (eventNameInput.value.trim() === '') {
          isEmpty = true;
          $(eventNameInput).addClass('border-red');
      } else{
        $(eventNameInput).removeClass('border-red');
      }
    }); 
    datePickerInputs.forEach(datePickerInput => {
    // Check if the input field is empty
      if (datePickerInput.value.trim() === '') {
          isEmpty = true;
          $(datePickerInput).addClass('border-red');
      } else {
        $(datePickerInput).removeClass('border-red');
      }
    });  

    for(let i = 0; i < startTimeInputs.length; i++){
      if(startTimeInputs[i].value >= endTimeInputs[i].value){
        console.log(startTimeInputs[i]);
        console.log(endTimeInputs[i]);
        $(startTimeInputs[i]).addClass('border-red');
        $(endTimeInputs[i]).addClass('border-red');
        timeCheck = true;
      }else{
        $(startTimeInputs[i]).removeClass('border-red');
        $(endTimeInputs[i]).removeClass('border-red');
      }
      console.log(timeCheck);
    }
    if (isEmpty){
      $('#textNotifierPadding').addClass('pt-5');
      $('.invalidFeedback').text("Event name or date field is empty");
      $('.invalidFeedback').css('display', 'block');  
      $('.invalidFeedback').on('animationend', function() {
        $('.invalidFeedback').css('display', 'none');
        $('#textNotifierPadding').removeClass('pt-5')
      });
      isEmpty = false;  
    }
    else if(timeCheck){
      $('#textNotifierPadding').addClass('pt-5');
      $('.invalidFeedback').text("Event end time must be after start time");
      $('.invalidFeedback').css('display', 'block');  
      $('.invalidFeedback').on('animationend', function() {
        $('.invalidFeedback').css('display', 'none');
        $('#textNotifierPadding').removeClass('pt-5')
      });
      timeCheck= false;
        
    }
    else {
      storeMultipleOfferingEventAttributes();
      pendingmultipleEvents = [];
      $("#checkIsSeries").prop('checked', true);
      // Remove the modal and overlay from the DOM
      $('#nonRepeatingSeries').modal('hide');
      $('.invalidFeedback').css('display', 'none');
      $('#textNotifierPadding').removeClass('pt-5');
      msgFlash("Multiple time offering events saved!", "success");
    }
  });
//build multi-event table
function storeMultipleOfferingEventAttributes() {
    let entries = [];
    $(".extraSlots").children().each(function(index, element) {
        let rowData = $.map($(element).find("input"), (el) => $(el).val());

        entries.push({
            eventName: rowData[0],
            eventDate: rowData[1],
            startTime: rowData[2],
            endTime: rowData[3]
        });
    });

    let entriesJson = JSON.stringify(entries);
    console.log(entriesJson);
    $("#seriesDataId").val(entriesJson);

  var nonRepeatingSeriesTable = $("#nonRepeatingSeriesTable");
  nonRepeatingSeriesTable.find("tbody tr").remove(); // Clear existing rows
  entries.forEach(function(entry){
    //fromat to 12hr time for display
    var formattedEventDate = formatDate(entry.eventDate);
    var startTime = format24to12HourTime(entry.startTime);
    var endTime = format24to12HourTime(entry.endTime);
    nonRepeatingSeriesTable.append("<tr><td>" + entry.eventName + "</td><td>" + formattedEventDate +"</td><td>" + startTime + "</td><td>" + endTime + "</td></tr>");
  });
}  
//visual date formatting for multi-event table
function formatDate(originalDate) {
  var dateObj = new Date(originalDate);
  //ensures that time zone is not inconsistent, keeping the date consistent with what the user selects
  dateObj.setUTCHours(0, 0, 0, 0);
  var month = dateObj.toLocaleString('default', { month: 'short' });
  var day = dateObj.getUTCDate();
  var year = dateObj.getUTCFullYear();
  return month + " " + day + ", " + year;
}
/*
 * Run when the webpage is ready for javascript
 */
$(document).ready(function() {
  //makes sure bonners toggle will stay on between event pages
  if (window.location.pathname == '/event/' + $('#newEventID').val() + '/edit') {
    if ($("#checkBonners")) {
      $("#checkBonners").prop('checked', true);
  }
}
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
  if ( $(".startDatePicker")[0].value != $(".endDatePicker")[0].value){
    calculateRepeatingEventFrequency();
  }
    handleFileSelection("attachmentObject")

  $("#checkRSVP").on("click", function () {
    if ($("#checkRSVP").is(":checked")) {
      $("#limitGroup").show();
    } else {
      $("#limitGroup").hide();
    }
  });
  // Determine which checkbox was clicked and its current checked status, uncheck others
  $("#checkIsTraining, #checkServiceHours, #checkBonners").on('click', function (event) {
    $("#checkIsTraining, #checkServiceHours, #checkBonners").not($(event.target)).prop('checked', false);
  });

  $("#saveEvent").on('submit', function (event) {
    let trainingStatus = $("#checkIsTraining").is(":checked")
    let serviceHourStatus = $("#checkServiceHours").is(":checked")
    let bonnersStatus = $("#checkBonners").is(":checked")
    //check if user has selected a toggle, cancel form submission if not
    if(trainingStatus || serviceHourStatus || bonnersStatus || $("#pageTitle").text() == 'Create All Volunteer Training'){
      // Disable button when we are ready to submit
      $(this).find("input[type=submit]").prop("disabled", true);
    }
    else {
      msgFlash("You must toggle event is a training, event earns service hours, or is a Bonners Scholars event!", "danger");
      event.preventDefault();
    } 
  });
  
  let modalOpenedByEditButton = false;
  
  //#checkIsRepeating, #checkIsSeries are attributes for the toggle buttons on create event page
  $("#checkIsRepeating, #checkIsSeries, #edit_modal").click(function(event) { 
    if(!($('#inputEventName').val().trim() == '')){
      //keeps main page event name for multiple event modal
      $('#eventName').val($('#inputEventName').val());
    }
    // retrieves toggle status, 'on' or undefined
    let repeatingStatus = $("#checkIsRepeating").is(":checked")
    let seriesStatus = $("#checkIsSeries").is(":checked")
    modalOpenedByEditButton = ($(this).attr('id') === 'edit_modal');


    if (seriesStatus == true && repeatingStatus == true){
      msgFlash("You may not toggle recurring event and multiple time offering event at the same time!", "danger");
      $(event.target).prop('checked', false);
      return; 
    }
    if (repeatingStatus == true) {
      $(".endDateStyle, #repeatingTableDiv").removeClass('d-none');
      $("#checkIsSeries").prop('checked', false);
      $('#nonRepeatingSeriesTableDiv').addClass('d-none');
      $(".endDatePicker").prop('required', true);
    } 

    else if (seriesStatus == true) {
      $(".startDatePicker").prop('required', false);
      $("#nonRepeatingSeriesTableDiv").removeClass('d-none');
      $("#checkIsRepeating").prop('checked', false);
      $(".endDateStyle, #repeatingTableDiv").addClass('d-none');
      $('#nonRepeatingSeries').modal('show');
      //hides the non multiple offering time and dates and replace
      $('#nonSeriesTime, #nonSeriesDate').addClass('d-none'); 
    }
    else { 
      //adds the display none button of bootstrap so that the end-date div disappears for repeating even
      $(".endDateStyle, #repeatingTableDiv").addClass('d-none');
      $(".endDatePicker").prop('required', false);
      //set page UI back to default
      $("#nonRepeatingSeriesTableDiv").addClass('d-none');
      $('#nonRepeatingSeries').modal('hide');
      $('#nonSeriesTime, #nonSeriesDate').removeClass('d-none');
      $(".startDatePicker").prop('required', true);
    }
  });

  //untoggles the button when the modal cancel or close button is clicked
  $("#cancelModalPreview, #multipleOfferingXbutton").click(function(){ 
    if (modalOpenedByEditButton == false) {
      $("#checkIsSeries").prop('checked', false);
      $('#nonSeriesTime, #nonSeriesDate').removeClass('d-none');
      $("#nonRepeatingSeriesTableDiv").addClass('d-none');
      $('#nonRepeatingSeries').modal('hide');
      $('.extraSlots').children().not(':first').remove();
    }
    pendingmultipleEvents.forEach(function(element){
      element.remove();

    });
  });
  
  /*cloning the div with ID nonRepeatingSeriesEvent and cloning, changing the ID of each clone going up by 1. This also changes 
  the ID of the deleteNonRepeatingSeriesEvent so that when the trash icon is clicked, that specific row will be deleted*/
  let counterAdd = 0 // counter to add customized ids into the newly created slots
  $(".addMultipleOfferingEvent").click(function(){
    let clonedMultipleOffering = $("#nonRepeatingSeriesEvent").clone();
    let newMultipleObject = clonedMultipleOffering.attr("id", "nonRepeatingSeriesEvent" + counterAdd)
    clonedMultipleOffering.find("#deleteNonRepeatingSeriesEvent").attr("id", "deleteNonRepeatingSeriesEvent" + counterAdd).removeClass('d-none');
    $(".extraSlots").append(clonedMultipleOffering);
    pendingmultipleEvents.push(newMultipleObject);
    //stripes event sections in event modal
    if(counterAdd % 2 == 0){
        newMultipleObject.css('background-color', '#f2f2f2');  
      }
      else{
        newMultipleObject.css('background-color', '#fff');  
      }
      counterAdd += 1
    //this is so that the trash icon can be used to delete the event
    clonedMultipleOffering.on("click", "[id^=deleteNonRepeatingSeriesEvent]", function() {
      // Extract the numeric part from the id
      var id = $(this).attr('id').match(/\d+/)[0]; 
      $("#nonRepeatingSeriesEvent" + id).remove(); 
    });
  });

  $("#allowPastStart").click(function() {
    var minDate = $("#allowPastStart:checked").val() ? new Date('10/25/1999') : new Date()
    $("#startDatePicker-main").datepicker("option", "minDate", minDate)
  })

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
      calculateRepeatingEventFrequency();
    }
  });

  var facilitatorArray = []
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

  $("#inputCharacters").keyup(function (event) {
    setCharacterLimit(this, "#remainingCharacters");
  });

  setCharacterLimit($("#inputCharacters"), "#remainingCharacters"); 
});
