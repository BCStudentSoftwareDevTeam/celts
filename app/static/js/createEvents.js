import searchUser from './searchUser.js'
let pendingmultipleEvents = []

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

function format12to24HourTime(timeStr) {
  // break the time into hours, minutes, and meridian (AM, PM)
  const [timePart, meridian] = timeStr.split(" ");
  let [hours, minutes] = timePart.split(":").map(Number);

  if (meridian === "PM" && hours !== 12) {
      hours += 12;
  } else if (meridian === "AM" && hours === 12) {
      hours = 0; // midnight
  }

  // format hours and minutes to always be 2 digits
  const formattedHours = hours.toString().padStart(2, "0");
  const formattedMinutes = minutes.toString().padStart(2, "0");

  return `${formattedHours}:${formattedMinutes}`;
}

function calculateRepeatingEventFrequency(){
  var eventDatesAndName = {name:$("#repeatingEventsNamePicker").val(),
                            isRepeating: true,
                            startDate:$("#repeatingEventsStartDate").val(),
                            endDate:$("#repeatingEventsEndDate").val()}
  $.ajax({
    type:"POST",
    url: "/makeRepeatingEvents",
    //get the startDate, endDate and name as a dictionary
    data: eventDatesAndName,
    success: function(jsonData){
      var generatedEvents = JSON.parse(jsonData)
      $("#generatedEventsTable tbody tr").remove();
      for(var event of generatedEvents){
        loadRepeatingOfferingToModal(event)
      }
      $("#generatedEvents").removeClass("d-none");
    },
    error: function(error){
      console.log(error)
      displayNotification("Failed to generate events.");
    }
  });
}

function setViewForSingleOffering(){
  $(".startDatePicker").prop('required', true);
  $("#multipleOfferingTableDiv").addClass('d-none');
  $('#eventTime, #eventDate').removeClass('d-none');
  $('#checkIsSeriesToggleContainer').addClass('col-md-6')
  $('#checkIsSeriesToggleContainer').removeClass('col-md-12')
}

function setViewForSeries(){
  $(".startDatePicker").prop('required', false);
  $("#multipleOfferingTableDiv").removeClass('d-none');
  $('#eventTime, #eventDate').addClass('d-none');
  $('#checkIsSeriesToggleContainer').removeClass('col-md-6')
  $('#checkIsSeriesToggleContainer').addClass('col-md-12')
  $("#pastDateWarningText").text("")
}

function displayNotification(message) {
  $('#textNotifierPadding').addClass('pt-5');
  $('.invalidFeedback').text(message);
  $('.invalidFeedback').css('display', 'block');  
  $('.invalidFeedback').on('animationend', function() {
    $('.invalidFeedback').css('display', 'none');
    $('#textNotifierPadding').removeClass('pt-5')
  });
}

function isDateInPast(dateString, timeString) {
  const combineDateTime = `${dateString}T${timeString}:00`;
  const setDate = new Date(combineDateTime).getTime();
  const today = Date.now();
  return setDate < today;
}

function initializeFlatpickr(obj) {
  flatpickr(obj, {
    enableTime: true,
    wrap: true,
    noCalendar: true,
    dateFormat: "h:i K",
    time_24hr: false,
    minTime: "08:00",
    maxTime: "22:00",
    minuteIncrement: 15,
    allowInput: true 
  });
}

function createOfferingModalRow({eventName=null, eventDate=null, startTime=null, endTime=null}={}){

  let clonedOffering = $("#multipleOfferingEvent").clone().removeClass('d-none').removeAttr("id");

  // insert values for the newly created row
  if (eventName) {clonedOffering.find('.multipleOfferingNameField').val(eventName)}
  if (eventDate) {clonedOffering.find('.multipleOfferingDatePicker').val(eventDate)}
  if (startTime) {clonedOffering.find('.multipleOfferingStartTime').val(startTime)}
  if (endTime) {clonedOffering.find('.multipleOfferingEndTime').val(endTime)}
  
  $("#multipleOfferingSlots").append(clonedOffering);
  pendingmultipleEvents.push(clonedOffering);

  if (navigator.userAgent.indexOf("Chrome") == -1) {
    initializeFlatpickr(clonedOffering.find('#flatpickr1'))
    initializeFlatpickr(clonedOffering.find('#flatpickr2'))
    $(".timepicker").prop("type", "text");
    $(".timeIcons").prop("hidden", false);

    var formattedStartTime = format24to12HourTime(clonedOffering.find(".multipleOfferingStartTime").prop("defaultValue"));
    var formattedEndTime = format24to12HourTime(clonedOffering.find(".multipleOfferingEndTime").prop("defaultValue"));
    clonedOffering.find(".multipleOfferingStartTime").val(formattedStartTime);
    clonedOffering.find(".multipleOfferingEndTime").val(formattedEndTime);
  }

  /* still necessary? seems like it's already doing this somewhere
   
  //this is so that the trash icon can be used to delete the event
  clonedMultipleOffering.find(".deleteMultipleOffering").on("click", function() {
    let attachedRow = $(this).closest(".eventOffering")
    attachedRow.animate({
        opacity: 0,
        height: '0px'
    }, 500, function() {
        // After the animation completes, remove the row
        attachedRow.remove();
    });
  });
  */
  return clonedOffering
}

function verifyRepeatingFields(){
  // verifies all fields in the repeating table are not empty.
  let repeatingFields = $(".repeatingEventsField");
  let isEmpty = false;
 enableLiveCustomValidityClearing();

  repeatingFields.each(function() {
    let value = $(this).val();
    if (value === "" || value == null){
      this.setCustomValidity("Please fill out the required field"); // do these actions
      this.reportValidity();
      isEmpty = true;
    } else {
      this.setCustomValidity("");
    }
  });
  return isEmpty
}

$('#saveSeries').on('click', function(e) {
  e.preventDefault(); // Prevent default form submission at the start
  enableLiveCustomValidityClearing()
  let eventOfferings = $('#multipleOfferingSlots .eventOffering');
  let eventNameInputs = $('#multipleOfferingSlots .multipleOfferingNameField');
  let datePickerInputs = $('#multipleOfferingSlots .multipleOfferingDatePicker');
  let startTimeInputs = $('#multipleOfferingSlots .multipleOfferingStartTime');
  let endTimeInputs = $('#multipleOfferingSlots .multipleOfferingEndTime');
  let isRepeatingStatus = $("#checkIsRepeating").is(":checked");
  let startDateInput = $("#repeatingEventsStartDate");
  let endDateInput = $("#repeatingEventsEndDate");
  
  let hasErrors = false; 
  
  // Validate repeating events fields first if it's a repeating event
  if (isRepeatingStatus) {
    if (verifyRepeatingFields()) {
      hasErrors = true;
    }
    
    // Check if start date is before end date for repeating events
    let startDate = new Date(startDateInput.val());
    let endDate = new Date(endDateInput.val());
    
    if (endDate <= startDate) {
      hasErrors = true;
      $(startDateInput).addClass('border-red');
      $(endDateInput).addClass('border-red');
      displayNotification("The end date must be after the start date.");
    } else {
      $(startDateInput).removeClass('border-red');
      $(endDateInput).removeClass('border-red');
    }
    
  } else {
    // Validate individual event offerings for non-repeating events
    // Check event name fields
    eventNameInputs.each((index, eventNameInput) => {
      if (eventNameInput.value.trim() === '') {
        hasErrors = true;
        $(eventNameInput)[0].setCustomValidity("Please enter an event name");
        $(eventNameInput)[0].reportValidity();
      } else {
        $(eventNameInput)[0].setCustomValidity("");
      }
    });

    // Check date picker fields
    datePickerInputs.each((index, datePickerInput) => {
      if (datePickerInput.value.trim() === '') {
        hasErrors = true;
        $(datePickerInput)[0].setCustomValidity("Please enter an event date");
        $(datePickerInput)[0].reportValidity();
      } else {
        $(datePickerInput)[0].setCustomValidity("");
      }
    });

    
    let hasTimeErrors = false;
    // Check if start time is before end time for each event
    for(let i = 0; i < startTimeInputs.length; i++){
      let startTime = startTimeInputs[i].value;
      let endTime = endTimeInputs[i].value;
      
      
      if (navigator.userAgent.indexOf("Chrome") == -1) {
        startTime = format12to24HourTime(startTime);
        endTime = format12to24HourTime(endTime);
      }

      if(startTime >= endTime){
        hasTimeErrors = true;
        startTimeInputs[i].classList.add('border-red');
        endTimeInputs[i].classList.add('border-red');
      } else {
        startTimeInputs[i].classList.remove('border-red');
        endTimeInputs[i].classList.remove('border-red');
      }
     }
     if (hasTimeErrors) {
      hasErrors = true;
      displayNotification("Event end time must be after start time");
    }

    // Check for duplicate event offerings
    let eventListings = {};
    for(let i = 0; i < eventOfferings.length; i++){
      let eventName = eventNameInputs[i].value;
      let date = datePickerInputs[i].value.trim();
      let startTime = startTimeInputs[i].value;
      let eventListing = JSON.stringify([eventName, date, startTime]);

      if (eventListing in eventListings){
        hasErrors = true;
        displayNotification("Event listings cannot have the same event name, date, and start time");
        break; // Exit loop on first duplicate found
      } else {
        eventListings[eventListing] = i;
      }
    }
  }

  // Only proceed if there are no validation errors
  if (!hasErrors) {
    saveOfferingsFromModal();
    $('#textNotifierPadding').removeClass('pt-5');
    updateOfferingsTable();
    pendingmultipleEvents = [];
    $("#pastDateWarningText").text("");
    $("#checkIsSeries").prop('checked', true);
    updateEventNameField();
    $('#modalSeries').modal('hide');
    msgFlash("You have successfully updated a series of events", "success");
  }
});

// Populate the Event Name field in the main page with the entered repeating events
function updateEventNameField() {
  let offerings = JSON.parse($("#seriesData").val())
  let isSeries = $("#checkIsRepeating").is(":checked")

  // Check if the event is weekly
  if (!isSeries) {
    // if not weeekly, add them to a set to remove duplicates, then put them in a string to populate the field
    let names = new Set()
    offerings.forEach(offering => {
      names.add(offering.eventName)
    });
    let offeringsText = Array.from(names).join(", ")
    $('#inputEventName').prop('placeholder', offeringsText)
  }
  else {
    // if weekly, take the name of the first item (which is the same for all) and take the word 'week'
    let offeringText = $("#repeatingEventsNamePicker").val()
    $('#inputEventName').prop('placeholder', offeringText)
  } 
}

// Save the offerings from the modal to the hidden input field
function saveOfferingsFromModal() {
  let offerings = [];
  let isRepeatingStatus = $("#checkIsRepeating").is(":checked");
  $("#formIsRepeating").prop("checked", isRepeatingStatus);
  let dataTable = isRepeatingStatus ? "#generatedEventsList" : "#multipleOfferingSlots";
  $(dataTable).children().each(function(index, element) {
    let rowData;
    if (isRepeatingStatus){
      rowData = $.map($(element).find("td"), function(td){
        let input = $(td).find("input");
        if (input.length){
          return input.val();
        } else {
          return $(td).text().trim();
        }
      })}
    else {
      rowData = $.map($(element).find("input"), (el) => $(el).val());
    }

    let startTime = isRepeatingStatus ? $("#repeatingEventsStartTime").val() : rowData[2]
    let endTime = isRepeatingStatus ? $("#repeatingEventsEndTime").val() : rowData[3]
    if (navigator.userAgent.indexOf("Chrome") == -1) {
        startTime = format12to24HourTime(startTime)
        endTime = format12to24HourTime(endTime)
    }
    offerings.push({
        eventName: rowData[0],
        eventDate: rowData[1],
        startTime: startTime,
        endTime: endTime,
    })
  });


  $(dataTable).children().remove();
  let offeringsJson = JSON.stringify(offerings);
  $("#seriesData").val(offeringsJson);
}

function loadOfferingsToModal(){
  let offerings = JSON.parse($("#seriesData").val())
  if (offerings.length < 1) {return;}
  let isRepeatingStatus = $("#checkIsRepeating").is(":checked");
  if (isRepeatingStatus) {$("#generatedEvents").removeClass("d-none"); $("#generatedEventsTable tbody tr").remove();};
  offerings.forEach((offering, i) =>{
    if (isRepeatingStatus){
      loadRepeatingOfferingToModal(offering);
    } else {
      let newOfferingModalRow = createOfferingModalRow(offering);
      //stripes odd event sections in event modal
      newOfferingModalRow.css('background-color', i % 2 ?'#f2f2f2':'#fff');
    }})
}


function loadRepeatingOfferingToModal(offering){
  var seriesTable = $("#generatedEventsTable");
  var eventDate = new Date(offering.date || offering.eventDate).toLocaleDateString();
  seriesTable.append(
    "<tr class='eventOffering'>" +
    "<td id='offeringName'>" + (offering.name || offering.eventName) + "</td>" + 
    "<td id='offeringDate'>" + eventDate + "</td>" +
    "<td><div class='deleteGeneratedEvent'><span class='bi bi-trash btn btn-danger'></span></div></td>" +
    "</tr>"
  );
}

// Update the table of offerings with the offerings from the hidden input field
function updateOfferingsTable() {
  let offerings = JSON.parse($("#seriesData").val())
  var offeringsTable = $("#offeringsTable");
  offeringsTable.find("tbody tr").remove(); // Clear existing rows
  offerings.forEach(function(offering){
    //format to 12hr time for display
    var formattedEventDate = formatDate(offering.eventDate);
    var startTime = format24to12HourTime(offering.startTime);
    var endTime = format24to12HourTime(offering.endTime);
    offeringsTable.append(`<tr class="${offering.isDuplicate ? "border-red" : ""}">` +
                                    "<td>" + offering.eventName + "</td>" +
                                    "<td>" + formattedEventDate + "</td>" +
                                    "<td>" + startTime + "</td>" +
                                    "<td>" + endTime + "</td>" +
                                  "</tr>"
                                );
  });
}

//visual date formatting for multi-event table
function formatDate(originalDate) {
  var dateObj = new Date(originalDate);
  // dateObj.setUTCHours(0, 0, 0, 0); // set the timezone

  var month = dateObj.toLocaleString('default', { month: 'short' });
  var day = dateObj.getUTCDate();
  var year = dateObj.getUTCFullYear();
  return month + " " + day + ", " + year;
}

function enableLiveCustomValidityClearing() {
  const allSelectors = [".all", ".series", ".seriesWeekly", ".main", ".allV", ".repeatingEventsField", ".multipleOfferingNameField"];
//Created the 
  allSelectors.forEach(selector => {
    $(selector).each(function () {
      // Avoid rebinding listeners on already-bound elements
      if (!$(this).data("has-clearing-listener")) {
        $(this).on("input", function () {
          this.setCustomValidity("");
        });
        $(this).data("has-clearing-listener", true); // flag it
      }
    });
  });
}

function validateFieldGroup(selector, allFieldFilled, message="Please fill out the required field") {
  let isValid = allFieldFilled;
  
  $(selector).each(function() {
    // Skip hidden or disabled fields
    if (!$(this).is(":visible") || $(this).is(":disabled")) return;
    
    // Skip event type checkboxes from regular validation
    let elementId = $(this).prop("id");
    if (elementId === "checkIsTraining" || elementId === "checkServiceHours" || 
        elementId === "checkEngagement" || elementId === "checkBonners") {
      return;
    }

    // Check if field is empty (excluding spaces)
    if ($(this).val().trim() === "") {
      this.setCustomValidity(message);
      this.reportValidity();
      isValid = false;
    } else {
      this.setCustomValidity("");
    }
  });
  
  return isValid;
}

function validateEventTypeCheckboxes(message="Please select at least one of the event options.") {
  let trainingStatus = $("#checkIsTraining").is(":checked");
  let serviceHourStatus = $("#checkServiceHours").is(":checked");
  let engagementStatus = $("#checkEngagement").is(":checked");
  let bonnersStatus = $("#checkBonners").is(":checked");
  
  if (!(trainingStatus || serviceHourStatus || engagementStatus || bonnersStatus)) {
    $("#checkEngagement")[0].setCustomValidity(message);
    $("#checkEngagement")[0].reportValidity();
    return false;
  } else {
    $("#checkEngagement")[0].setCustomValidity("");
    return true;
  }
}

function checkValidation() {
  let allFieldFilled = true;
  let seriesEvent = $("#checkIsSeries").is(":checked");
  let seriesWeeklyId = $("#checkIsRepeating").is(":checked");
  let isAllVolunteer = $("#pageTitle").text() == 'Create All Volunteer Training';
  
  enableLiveCustomValidityClearing();

  // Always validate common fields (.all class)
  allFieldFilled = validateFieldGroup(".all", allFieldFilled);
  
  if (seriesEvent) {
    // Validate series-specific fields
    allFieldFilled = validateFieldGroup(".series", allFieldFilled);
    
    // Validate series weekly fields if needed
    if (seriesWeeklyId) {
      allFieldFilled = validateFieldGroup(".seriesWeekly", allFieldFilled);
    }
    
    // Validate event type checkboxes
    allFieldFilled = validateEventTypeCheckboxes() && allFieldFilled;
    
  } else if (isAllVolunteer) {
    // Validate all volunteer specific fields
    allFieldFilled = validateFieldGroup(".allV", allFieldFilled);
    
  } else {
    // Validate main template fields
    allFieldFilled = validateFieldGroup(".main", allFieldFilled);
    
    // Validate event type checkboxes
    allFieldFilled = validateEventTypeCheckboxes() && allFieldFilled;
  }
  
  // Submit form if all fields are valid
  if (allFieldFilled) {
    const form = $("#saveEvent");
    if (form.length) {
      form.trigger('submit');
    }
  }
}



/*
 * Run when the webpage is ready for javascript
 */
$(document).ready(function() {
  var isEditPage = (window.location.pathname == '/event/' + $('#newEventID').val() + '/edit')

  //makes sure bonners toggle will stay on between event pages
  if (isEditPage) {
    if ($("#checkBonners")) {
      $("#checkBonners").prop('checked', true);
    }
  }

  // don't use a minimum if we are editing an existing event
  var minDate = new Date()
  if (isEditPage) {
      minDate = null;
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
  let typeBoxes = $("#checkIsTraining, #checkServiceHours, #checkEngagement, #checkBonners")
  typeBoxes.on('click', function (event) {
    typeBoxes.not($(event.target)).prop('checked', false);
  });

  //to show the msgFlash message when the event is canceled
$("#cancelEvent").on('click', function (event) {
    event.preventDefault(); // Prevent normal form submission
    
    // Get the form action URL
    let formAction = $(this).closest('form').attr('action');
    
    // Submit via AJAX
    $.ajax({
        url: formAction,
        method: 'POST',
        success: function(response) {
            msgFlash("You have successfully canceled the event", "success", 5000);
            $('#cancelWarning').modal('hide');
            // Optionally refresh the page or update the UI
            location.reload(); // or update specific elements
        },
        error: function() {
            msgFlash("Failed to cancel the event", "error");
        }
    });
});

  // When Save buttton is clicked, check if required are filled and then submit
  $("#saveButton").on('click', function (event) {
    event.preventDefault(); //prevents from submitting
    checkValidation();
});
  
  updateOfferingsTable();
  
  if ($("#checkIsSeries").is(":checked")){
    setViewForSeries();
  }
  
  let modalOpenedByEditButton = false;
  //#checkIsRepeating, #checkIsSeries are attributes for the toggle buttons on create event page
  $("#checkIsSeries, #edit_modal").click(function(event) {

    if(!($('#inputEventName').val().trim() == '')){
      //keeps main page event name for multiple event modal
      $('#eventName').val($('#inputEventName').val());// the input value from of page copied
    }
    let isSeries = $("#checkIsSeries").is(":checked")
    modalOpenedByEditButton = ($(this).attr('id') === 'edit_modal');

    if (isSeries) {
      setViewForSeries();
      loadOfferingsToModal();
      $('#modalSeries').modal('show');

      // Disable single event name field
      $('#inputEventName').prop('readonly', true)
      $('#inputEventName').val('')
    } else {
      setViewForSingleOffering()
      $('#multipleOfferingTableDiv').addClass('d-none');
      // Enable single event name field
      $('#inputEventName').prop('readonly', false)
      $('#inputEventName').prop('placeholder', 'Enter event name')  
    }
  });

  //untoggles the button when the modal cancel or close button is clicked
  $("#cancelModalPreview, #multipleOfferingXbutton").click(function(){ 
    if (modalOpenedByEditButton == false) {
      $('#modalSeries').modal('hide');
      $("#checkIsSeries").prop('checked', false);
      setViewForSingleOffering()
    }
    pendingmultipleEvents.forEach(function(element){
      element.remove();
    });
    let isSeries = $("#checkIsSeries").is(":checked")
    if (!isSeries){
      // Enable single event name field
      $('#inputEventName').prop('readonly', false)
      $('#inputEventName').prop('placeholder', 'Enter event name')
      checkIfDateInPast();
    }
  });

  $("#checkIsRepeating").change(function() {
    if ($(this).is(':checked')) {
      $('.addMultipleOfferingEvent').hide();
      $("#repeatingEventsDiv").removeClass('d-none');
      $("#multipleOfferingSlots").children().remove();
      $("#multipleOfferingSlots").addClass('d-none');
    } else {
      $('.addMultipleOfferingEvent').show(); 
      $("#repeatingEventsDiv").addClass('d-none');
      $("#multipleOfferingSlots").removeClass('d-none');
    }
  });
  
  $("#repeatingEventsDiv").change(handleRepeatingEventsChange)
// this handels start date, end date, last event date, start time, and end time 
  function handleRepeatingEventsChange() {
    if (!verifyRepeatingFields()) {
      let table = $("#generatedEventsList").children();
      let startDate = new Date($("#repeatingEventsStartDate").val());
      let endDate = new Date($("#repeatingEventsEndDate").val());
      let startTime = $("#repeatingEventsStartTime").val();
      let endTime = $("#repeatingEventsEndTime").val();
      
      if (navigator.userAgent.indexOf("Chrome") == -1) { //CHANGES 12 HOUR TO 24 HOUR
        startTime = format12to24HourTime(startTime)
        endTime = format12to24HourTime(endTime)
      }

      if (endDate <= startDate) {
        displayNotification("The end date must be after the start date.");
        table.each(function(){$(this).remove()})
        $("#generatedEvents").addClass('d-none');
        return;
      }
      if (endTime <= startTime){
        displayNotification("The end time must be after the start time.");
        table.each(function(){$(this).remove()})
        $("#generatedEvents").addClass('d-none');
        return;
      }
      

      calculateRepeatingEventFrequency();
    }
  }

  $(document).on("click", ".deleteGeneratedEvent, .deleteMultipleOffering", function() {
    let attachedRow = $(this).closest(".eventOffering")
    attachedRow.animate({
      opacity: 0,
    }, 500, function() {
        // After the animation completes, remove the row
        attachedRow.remove();
        msgToast("Deletion info", "You have successfully deleted a series of events")
    });
  });
  
  /*cloning the div with ID multipleOfferingEvent and cloning, changing the ID of each clone going up by 1. This also changes 
  the ID of the deleteMultipleOffering so that when the trash icon is clicked, that specific row will be deleted*/
  $(".addMultipleOfferingEvent").click(createOfferingModalRow)

    var minDate = new Date('10/25/1999') 
    $("#startDatePicker-main").datepicker("option", "minDate", minDate)

  // This converts the time to 24 hour format in case it is in 12 hour format (like in Firefox)
function handleTimeFormatting(timeArray){    
  let time  = timeArray[0]
  let timeSuffix = timeArray[1]         // looks for AM or PM in time 
  let [hours , min] = time. split(':')

  if (timeArray.length === 2) {
    hours  = parseInt(hours, 10)
    if (timeSuffix === 'PM' && hours !== 12) {
      hours += 12;
    } else if (timeSuffix === 'AM' && hours === 12) {
      hours = 0;
    }
    const hoursStr = hours.toString().padStart(2, '0');
    return [hoursStr, min]
  }
  return [hours, min]
}

  function checkIfDateInPast() {
    const [month, day, year] = $("#startDatePicker-main").val().split('/')
    const startTimeArray =  $("#startTime-main").val().split(' ') 
    const [startHour, startMin] = handleTimeFormatting(startTimeArray)
    const endTimeArray = $('#endTime-main').val().split(' ')
    const [endHour, endMin] = handleTimeFormatting (endTimeArray)
    let startDateSelected =new Date(+year, +month - 1, +day, +startHour, +startMin);  
    let endDateSelected = new Date(+year, +month - 1, +day, +endHour, +endMin)
    let now = new Date()
    

    if (startDateSelected < now && endDateSelected > now) {
      $("#pastDateWarningText").text("This event is currently in progress!")
    }
    else if (startDateSelected < now && endDateSelected < now) {
      $("#pastDateWarningText").text("This event is in the past!")
    }
    else 
      $("#pastDateWarningText").text("")
  }

  $("#startDatePicker-main").on("change", function() {    
    checkIfDateInPast()
  })

  $("#startTime-main").on("change", function() {    
    checkIfDateInPast()
  })
  
  $("#endTime-main").on("change", function() {    
    checkIfDateInPast()
  })

  // everything except Chrome
  if (navigator.userAgent.indexOf("Chrome") == -1) {
    initializeFlatpickr(".flatpickr")
    
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

  $(".readonly").on('keydown paste', function(e) {
    if (e.keyCode != 9) // ignore tab
      e.preventDefault();
  });

  $(".startDate").click(function () {
    $("#startDatePicker-" + $(this).data("page-location")).datepicker("show");
  });

  $(".endDate").click(function () {
    $("#endDatePicker-" + $(this).data("page-location")).datepicker("show");
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

  $("#inputCharacters").keyup(function () {
    setCharacterLimit(this, "#remainingCharacters");
  });

  setCharacterLimit($("#inputCharacters"), "#remainingCharacters"); 
  
});




