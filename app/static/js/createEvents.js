import searchUser from './searchUser.js'



// updates max and min dates of the datepickers as the other datepicker changes
function updateDate(obj) {
  // we need to replace "-" with "/" because firefox cannot turn a date with "-" to a datetime object
  var selectedDate = ($(obj).val()).replaceAll("-", "/")
  var dateToChange = new Date(selectedDate);
  var newMonth = dateToChange.getMonth();
  var newYear = dateToChange.getFullYear();
  var newDay = dateToChange.getDate();
  if(obj.className.includes("startDatePicker")) {
    $("#endDatePicker-"+$(obj).data("page-location")).datepicker({minDate: new Date(newYear, newMonth, newDay)});
    $("#endDatePicker-"+$(obj).data("page-location")).datepicker("option", "minDate", new Date(newYear, newMonth, newDay));
  }
  if (obj.className.includes("endDatePicker")) {
    $("#startDatePicker-"+$(obj).data("page-location")).datepicker({maxDate: new Date(newYear, newMonth, newDay)});
    $("#startDatePicker-"+$(obj).data("page-location")).datepicker("option", "maxDate", new Date(newYear, newMonth, newDay));
  }
}

// turns a string with a time with HH:mm format to %I:%M %p format
// used to display 12 hour format but still use 24 hour format in the backend
function format24to12HourTime(timeStr){
  var formattedTime;
    if (parseInt(timeStr.slice(0, 2)) > 12){
      formattedTime = "0" + String(parseInt(timeStr.slice(0, 2)) - 12) + timeStr.slice(2) + " PM";
    }
    else if (parseInt(timeStr.slice(0, 2)) < 12 ){
      formattedTime =  timeStr + " AM";
    }
    else {
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
    // Call the function storingCustomEventAttributes() when the button is clicked
    storingCustomEventAttributes();
    $("#checkIsCustom").prop('checked', true);
    // Remove the modal and overlay from the DOM
    $('#modalCustom').modal('hide');
});

function storingCustomEventAttributes() {
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

    console.log(entries);
    console.log(typeof entires)

    let entriesJson = JSON.stringify(entries);
    document.getElementById("customEventsDataId").value = entriesJson

  var customTable = $("#customEventsTable");
  customTable.find("tbody tr").remove(); // Clear existing rows
  entries.forEach(function(entry){
    //fromat to 12hr time for display
    var startTime = format24to12HourTime(entry.startTime);
    var endTime = format24to12HourTime(entry.endTime);
    customTable.append("<tr><td>" + entry.eventName + "</td><td>" + entry.eventDate +"</td><td>" + startTime + "</td><td>" + endTime + "</td></tr>");
  });
}  

// $.ajax({
//   type: "POST",
//   url: "/makeCustomEvents",
//   data: { events: entries }, // Send data as an object
//   success: function(jsonData) {
//       console.log("success AJAX call");
//       console.log(jsonData);

//       var customEvents = JSON.parse(jsonData);
//       var customTable = $("#customEventsTable");
//       customTable.find("tbody tr").remove(); // Clear existing rows

//       console.log("Data Type of", typeof customEvents);
//       console.log(customEvents);

//       // Check if customEvents is an object
//       if (typeof customEvents === 'object' && !Array.isArray(customEvents)) {
//           // Iterate over the properties of the object using for...in
//           for (var key in customEvents) {
//               console.log(key)
//               if (customEvents.hasOwnProperty(key)) {
//                   var event = customEvents[key];
//                   console.log(event)
//                   var eventDate = new Date(event.date).toLocaleDateString();
//                   var startTime = event.startTime;
//                   var endTime = event.endTime;

//                   customTable.append("<tr><td>" + event.name + "</td><td><input name='eventdate" + eventDate + "' type='hidden' value='" + eventDate + "'>" + eventDate + "</td><td>" + startTime + "</td><td>" + endTime + "</td></tr>");
//               }
//           }
//       } else {
//           console.error("customEvents is not an object:", customEvents);
//       }
//   },
//   error: function(error) {
//       console.log(error);
//   }
// });
    // var customDatesAndTimes = {
    //   name: $("#inputEventName").val(),
    //   isCustom: true,
    //   customDate: $("#customDatePicker" + pageLocation).val(),
    //   startTime: $("#customstartTime-" + pageLocation).val(),
    //   endTime: $("#customendTime-" + pageLocation).val()
    // };

    // console.log('customDatesAndTime:' , customDatesAndTimes);
      
    //   $.ajax({
    //   type:"POST",
    //   url: "/makeCustomEvents",
    //   data: customDatesAndTimes, //get the customDate, startTime, endTime as a dictionary
    //   success: function(jsonData){
    //   var customEvents = JSON.parse(jsonData)
    //   console.log('customEvents:', customEvents)
    //   var customTable = $("#customEventsTable")
    //   $("#customEventsTable tbody tr").remove();

    //   for (var event of customEvents){
    //   var eventdate = new Date(event.date).toLocaleDateString()
    //   customTable.append("<tr><td>"+event.name+"</td><td><input name='week"+event.week+"' type='hidden' value='"+eventdate+"'>"+eventdate+"</td></tr>");
    //   }
    //   },
    //   error: function(error){
    //   console.log(error)
    //   }
    //   });
    // }
  

    
    /*while (index < num.length || index < color.length || index < value.length) {
    // Retrieve elements from arrays if they exist at current index
    a = index < num.length ? num[index] : null;
    b = index < color.length ? color[index] : null;
    c = index < value.length ? value[index] : null;
    console.log(a, b, c);
    index++;
    }
    let customDate=[];
    let customStartTime=[];
    let customEndTime=[];
    for (let i = 1; i = $(".add_customevent").length; i++){
      customDate.append($(".add_customevent"+i).children("input#customDatePicker").value);
      customStartTime.append($(".add_customevent"+i).children("input.customstartTime").value);
      customEndTime.append($(".add_customevent"+i).children("input.customendTime").value);
    }
    var customDatesAndName = {name:$("#inputEventName").val(),
                              isRecurring: true,
                              startDate:$(".startDatePicker")[0].value,
                              endDate:$(".endDatePicker")[0].value}
    let index = 0;
    while (index < customDate.length || index < customStartTime.length || index < customEndTime){

    }
    var eventDatesAndName = {name:$("#inputEventName").val(),
      isCustom: true,
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

}*/

/*
 * Run when the webpage is ready for javascript
 */
$(document).ready(function() {
  if ( $(".startDatePicker")[0].value != $(".endDatePicker")[0].value){
    calculateRecurringEventFrequency();
  }
    handleFileSelection("attachmentObject")

    $("#checkRSVP").on("click", function() {
      if ($("#checkRSVP").is(":checked")) {
        $("#limitGroup").show();
      }
      else{
        $("#limitGroup").hide();
      }
    })
  // Disable button when we are ready to submit
  $("#saveEvent").on('submit',function(event) {
    $(this).find("input[type=submit]").prop("disabled", true);
  });

  $("#checkIsRecurring, #checkIsCustom").click(function() { //#checkIsRecurring, #checkIsCustom are attributes for the toggle buttons on create event page  createEvent.html line 157-160
    var recurringStatus = $("input[id='checkIsRecurring']:checked").val(); //this line function is to retrive ON when its toggle for recurring event on createEvent.html line 158
    var customStatus = $("input[id='checkIsCustom']:checked").val();// this line function is to retrive ON when toggle for custom event button createEvent.html line 160
    if (recurringStatus == 'on') {
      $(".endDateStyle, #recurringTableDiv").removeClass('d-none');// this line removes the display none button of bootstrap so that the end-date div appears for recurring event
      $(".endDatePicker").prop('required', true);
    } 
    else if (recurringStatus == undefined){
      $(".endDateStyle, #recurringTableDiv").addClass('d-none');// this line add the display none button of bootstrap so that the end-date div disappears for recurring event
      $(".endDatePicker").prop('required', false);
    }
    if (customStatus == 'on') {
      $('#modalCustom').modal('show');// this line pop up the modal for the custom event
      $('#nonCustomTime, #nonCustomDate').addClass('d-none'); // this line disappear the non custom tims and dates and replace them with recurring table div for custom events to show
      $("#customTableDiv").removeClass('d-none');
      $("#checkIsCustom").prop('checked', true);
    }
    else if (customStatus == undefined){
      $("#customTableDiv").addClass('d-none');
      $('#modalCustom').modal('hide');
    }
  });
  
  $(".btn-close, #cancelModalPreview").click(function(){ //this function is to untoggle the button when the modal has cancel or close button being clicked
    $("#checkIsCustom").prop('checked', false);
    $('#nonCustomTime, #nonCustomDate').removeClass('d-none');
    $("#customTableDiv").addClass('d-none');
    $('#modalCustom').modal('hide');
    $('.extraSlots').children().not(':first').remove();
    //$('.extraSlots').empty();//this line remove the added custom event slots from appearing if the custom modal is toggle again
  });
  
  /*cloning the div with ID customEvent and cloning, changing the ID of each clone going up by 1. This also changes the ID of the delete_customEvent so that when the trash icon is clicked, 
  that specific row will be deleted*/
  let counterAdd = 0 // counter to add customized ids into the newly created slots
  $(".add_customevent").click(function(){
    counterAdd += 1
    let clonedCustom = $("#customEvent").clone();// this line clones the customEvent id div in the custom event modal on createEvent.html line 403
    clonedCustom.attr("id", "customEvent" + counterAdd)
    clonedCustom.find("#delete_customevent").attr("id", "delete_customevent" + counterAdd).removeClass('d-none');
    $(".extraSlots").append(clonedCustom)

    //this is so that the trash icon can be used to delete the event
    clonedCustom.on("click", "[id^=delete_customevent]", function() {
      var id = $(this).attr('id').match(/\d+/)[0]; // Extract the numeric part from the id
      $("#customEvent" + id).remove(); 
    });
  });

  $("#allowPastStart").click(function() {
    var allowPast = $("#allowPastStart:checked").val()
    if (allowPast == 'on') {
      $.datepicker.setDefaults({
        minDate:  new Date('1999/10/25'),
        dateFormat:'mm-dd-yy'
      });
    } else {
      $.datepicker.setDefaults({
        minDate:  new Date($.now()),
        dateFormat:'mm-dd-yy'
      });
    }
  });

  // everything except Chrome
  if (navigator.userAgent.indexOf("Chrome") == -1) {
    $('input.timepicker').timepicker({
             timeFormat : 'hh:mm p',
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
    $(".startTime"[0]).val(formattedStartTime);
    $(".endTime"[0]).val(formattedEndTime);
  }
  else {
    $(".timepicker").prop("type", "time");
    $(".timeIcons").prop("hidden", true);
  }

  if ($(".datePicker").is("readonly")) {
    $(".datePicker" ).datepicker( "option", "disabled", true )
  };

  //makes the input fields act like readonly (readonly doesn't work with required)
  $(".readonly").on('keydown paste', function(e){
        if(e.keyCode != 9) // ignore tab
            e.preventDefault();
  });

  $.datepicker.setDefaults({
    minDate:  new Date($.now()),
    dateFormat:'mm-dd-yy'
  });

  $(".startDate").click(function() {
    $("#startDatePicker-" + $(this).data("page-location")).datepicker().datepicker("show");
  });

  $(".endDate").click(function() {
    $("#endDatePicker-" + $(this).data("page-location")).datepicker().datepicker("show");
  });

  $(".startDatePicker, .endDatePicker").change(function(){
    if ( $(this).val() && $("#endDatePicker-" + $(this).data("page-location")).val()){
      calculateRecurringEventFrequency();
    }
  });

  $("#checkRSVP").click(function(){
    if ($("input[name='isRsvpRequired']:checked").val() == 'on'){
      $("#checkFood").prop('checked', true);

    } else{
      $("#checkFood").prop('disabled', false);
    }
  });

  var facilitatorArray = []
  function callback(selectedFacilitator) {
    // JSON.parse is required to de-stringify the search results into a dictionary.
    let facilitator = (selectedFacilitator["firstName"]+" "+selectedFacilitator["lastName"]+" ("+selectedFacilitator["username"]+")");
    let username = selectedFacilitator["username"];
    if (!facilitatorArray.includes(username)){
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

  $("#eventFacilitator").on('input', function() {
    // To retrieve specific columns into a dict, create a [] list and put columns inside
    searchUser("eventFacilitator", callback, true, undefined, "instructor");
  });

  $("#facilitatorTable").on("click", "#remove", function() {
     let username = $(this).closest("tr")[0].id
     const index = facilitatorArray.indexOf(username)
     facilitatorArray.splice(index, 1);
     $("#hiddenFacilitatorArray").attr("value", facilitatorArray);
     $(this).closest("tr").remove();
  });

  $(".endDatePicker").change(function(){
     updateDate(this)
  });

  $(".startDatePicker").change(function(){
     updateDate(this)
  });

//   $(".customDatePicker").change(function(){ //custom data calender function
//     updateDate(this)
//  });

  $("#inputCharacters").keyup(function(event){
    setCharacterLimit(this, "#remainingCharacters")
    });

  setCharacterLimit($("#inputCharacters"), "#remainingCharacters");

});
