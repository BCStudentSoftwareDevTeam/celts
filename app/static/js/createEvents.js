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
  $('#nonMultipleOfferingTime, #nonMultipleOfferingDate').removeClass('d-none');
}

function setViewForMultipleOffering(){
  $(".startDatePicker").prop('required', false);
  $("#multipleOfferingTableDiv").removeClass('d-none');
  $('#nonMultipleOfferingTime, #nonMultipleOfferingDate').addClass('d-none');
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

function isDateInPast(dateString) {
  const date = new Date(dateString);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return date < today;
}

function createOfferingModalRow({eventName=null, eventDate=null, startTime=null, endTime=null, isDuplicate=false}={}){

  let clonedMultipleOffering = $("#multipleOfferingEvent").clone().removeClass('d-none').removeAttr("id");
  // insert values for the newly created row
  if (eventName) {clonedMultipleOffering.find('.multipleOfferingNameField').val(eventName)}
  if (eventDate) {clonedMultipleOffering.find('.multipleOfferingDatePicker').val(eventDate)}
  if (startTime) {clonedMultipleOffering.find('.multipleOfferingStartTime').val(startTime)}
  if (endTime) {clonedMultipleOffering.find('.multipleOfferingEndTime').val(endTime)}
  if (isDuplicate) {clonedMultipleOffering.addClass('border-red')}

  $("#multipleOfferingSlots").append(clonedMultipleOffering);
  pendingmultipleEvents.push(clonedMultipleOffering);

  return clonedMultipleOffering
}

$('#multipleOfferingSave').on('click', function() {
  //Requires that modal info updated before it can be saved, gives notifier if there are empty fields
  let eventOfferings = $('#multipleOfferingSlots .eventOffering');
  let eventNameInputs = $('#multipleOfferingSlots .multipleOfferingNameField');
  let datePickerInputs = $('#multipleOfferingSlots .multipleOfferingDatePicker');
  let startTimeInputs = $('#multipleOfferingSlots .multipleOfferingStartTime');
  let endTimeInputs = $('#multipleOfferingSlots .multipleOfferingEndTime');
  let isEmpty = false;
  let hasValidTimes = true;
  let hasDuplicateListings = false;
  let hasInvalidDates = false;
  const allowPastStart = $("#allowPastStart").is(":checked");


  // Check if the input field is empty
  eventNameInputs.each((index, eventNameInput) => {
    if (eventNameInput.value.trim() === '') {
      isEmpty = true;
      $(eventNameInput).addClass('border-red');
    } else{
      $(eventNameInput).removeClass('border-red');
    }
  });

  // Check if the date input field is empty
  datePickerInputs.each((index, datePickerInput) => {
    if (datePickerInput.value.trim() === '') {
        isEmpty = true;
        $(datePickerInput).addClass('border-red');
    } else {
      $(datePickerInput).removeClass('border-red');
    }
  });  


  // Check if the start time is after the end time
  for(let i = 0; i < startTimeInputs.length; i++){
    if(startTimeInputs[i].value < endTimeInputs[i].value){
      $(startTimeInputs[i]).removeClass('border-red');
      $(endTimeInputs[i]).removeClass('border-red');
    } else {
      $(startTimeInputs[i]).addClass('border-red');
      $(endTimeInputs[i]).addClass('border-red');
      hasValidTimes = false;
    }
  }

  // Check if there are duplicate event offerings
  let eventListings = {};
  for(let i = 0; i < eventOfferings.length; i++){
    let eventName = eventNameInputs[i].value
    let date = datePickerInputs[i].value.trim()
    let startTime = startTimeInputs[i].value
    let eventListing = JSON.stringify([eventName, date, startTime])

    if (eventListing in eventListings){ // If we've seen this event before mark this event and the previous as duplicates
      hasDuplicateListings = true
      $(eventOfferings[i]).addClass('border-red');
      $(eventOfferings[eventListings[eventListing]]).addClass('border-red')
    } else { // If we haven't seen this event before
      $(eventOfferings[i]).removeClass('border-red');
      eventListings[eventListing] = i
    }
  }

  // Add past date validation
  datePickerInputs.each(function(index, element) {
    if (!allowPastStart && isDateInPast($(element).val())) {
      $(element).addClass('border-red');
      hasInvalidDates = true;
    } else {
      $(element).removeClass('border-red');
    }
  }); 

  if (isEmpty){
    let emptyFieldMessage = "Event name or date field is empty";
    displayNotification(emptyFieldMessage);
  }
  else if (!hasValidTimes) {
    let invalidTimeMessage = "Event end time must be after start time";
    displayNotification(invalidTimeMessage);
  }
  else if (hasDuplicateListings) {
    let eventConflictMessage = "Event listings cannot have the same event name, date, and start time";
    displayNotification(eventConflictMessage);
  }
  else if (hasInvalidDates) {
    displayNotification ("Some events have dates in the past. Please correct them or enable 'Allow start date to be in the past'.", "danger");
  }
  else {
    saveOfferingsFromModal();
    $('#textNotifierPadding').removeClass('pt-5');
    updateOfferingsTable();
    pendingmultipleEvents = [];
    $("#checkIsSeries").prop('checked', true);
    // Remove the modal and overlay from the DOM
    $('#modalMultipleOffering').modal('hide');
    msgFlash("Multiple time offering events saved!", "success");
  }
});


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
      offerings.push({
        eventName: rowData[0],
        eventDate: rowData[1],
        startTime: isRepeatingStatus ? $("#repeatingEventsStartTime").val() : rowData[2],
        endTime: isRepeatingStatus ? $("#repeatingEventsEndTime").val() : rowData[3]
    })
  });

  $(dataTable).children().remove();
  let offeringsJson = JSON.stringify(offerings);
  $("#seriesData").val(offeringsJson); // huh?
}

function verifyRepeatingFields(){
  // verifies all fields in the repeating table are not empty.
  let repeatingFields = $(".repeatingEventsField");
  let allFieldsFilled = true;
  repeatingFields.each(function() {
    let value = $(this).val();
    if (value === "" || value == null){
      allFieldsFilled = false;
      return false;
    }
  })
  return allFieldsFilled
}

function loadOfferingsToModal(){
  let offerings = JSON.parse($("#seriesData").val())
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
    "<td><div class='deleteGeneratedEvent'><i class='bi bi-trash btn btn-danger'></i></div></td>" +
    "</tr>"
  );
}

// Update the table of offerings with the offerings from the hidden input field
function updateOfferingsTable() {
  let offerings = JSON.parse($("#seriesData").val())
  var offeringsTable = $("#offeringsTable");
  offeringsTable.find("tbody tr").remove(); // Clear existing rows
  offerings.forEach(function(offering){
    //fromat to 12hr time for display
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
$(".startDatePicker").change(function () {
  updateDate(this);
});

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

  updateOfferingsTable();
  
  if ($("#checkIsSeries").is(":checked")){
    setViewForMultipleOffering();
  }
  
  let modalOpenedByEditButton = false;
  //#checkIsRepeating, #checkIsSeries are attributes for the toggle buttons on create event page
  $("#checkIsSeries, #edit_modal").click(function(event) { 
    if(!($('#inputEventName').val().trim() == '')){
      //keeps main page event name for multiple event modal
      $('#eventName').val($('#inputEventName').val());
    }
    let multipleOfferingStatus = $("#checkIsSeries").is(":checked")
    modalOpenedByEditButton = ($(this).attr('id') === 'edit_modal');

    if (multipleOfferingStatus == true) {
      setViewForMultipleOffering();
      loadOfferingsToModal();
      $('#modalMultipleOffering').modal('show');
    } else {
      setViewForSingleOffering()
      $('#multipleOfferingTableDiv').addClass('d-none');
    }
 
  });

  //untoggles the button when the modal cancel or close button is clicked
  $("#cancelModalPreview, #multipleOfferingXbutton").click(function(){ 
    if (modalOpenedByEditButton == false) {
      $('#modalMultipleOffering').modal('hide');
      $("#checkIsSeries").prop('checked', false);
      setViewForSingleOffering()
    }
    pendingmultipleEvents.forEach(function(element){
      element.remove();
    });
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
  
  $("#repeatingEventsDiv").change(function() {
    if (verifyRepeatingFields()){
      let startDate = new Date($("#repeatingEventsStartDate").val());
      let endDate = new Date ($("#repeatingEventsEndDate").val());
      if (endDate <= startDate){
        displayNotification("Invalid dates.");
        return;
      }
      calculateRepeatingEventFrequency();
    }
  })

  $(document).on("click", ".deleteGeneratedEvent, .deleteMultipleOffering", function() {
    let attachedRow = $(this).closest(".eventOffering")
    attachedRow.animate({
      opacity: 0,
      height: '0px'
    }, 500, function() {
        // After the animation completes, remove the row
        attachedRow.remove();
    });
  });
  
  /*cloning the div with ID multipleOfferingEvent and cloning, changing the ID of each clone going up by 1. This also changes 
  the ID of the deleteMultipleOffering so that when the trash icon is clicked, that specific row will be deleted*/
  $(".addMultipleOfferingEvent").click(createOfferingModalRow)

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

  $("#inputCharacters").keyup(function () {
    setCharacterLimit(this, "#remainingCharacters");
  });

  setCharacterLimit($("#inputCharacters"), "#remainingCharacters"); 
});
