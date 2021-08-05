
$(document).ready(function(){

  $("#checkIsRecurring").click(function() {
    var recurringStatus = $("input[name='eventIsRecurring']:checked").val()
    if (recurringStatus == 'on'){
      $("#endDateStyle, #recurringTableDiv").removeClass('d-none')
      $("#endDatePicker").prop('required', true);


    }else{
      $("#endDateStyle, #recurringTableDiv").addClass('d-none')
      $("#endDatePicker").prop('required', false);
    }
  });

$(document).ready(function(){
  if($(".datePicker").is("readonly")){
    $( ".datePicker" ).datepicker( "option", "disabled", true );
}

});

  $(".readonly").on('keydown paste', function(e){ //makes the input fields act like readonly (readonly doesn't work with required)
        if(e.keyCode != 9) // ignore tab
            e.preventDefault();
    });

  $.datepicker.setDefaults({
    minDate:  new Date($.now()),
    dateFormat:'mm-dd-yy'
  });

  $("#startDate").click(function() {
    $("#startDatePicker").datepicker().datepicker("show"); // Shows the start date datepicker when glyphicon is clicked
  });

  $("#endDate").click(function() {
      $("#endDatePicker").datepicker().datepicker("show"); // Shows the start date datepicker when glyphicon is clicked
    });

    $("#startDatePicker, #endDatePicker").change(function(){

      if ( $("#startDatePicker").val() && $("#endDatePicker").val()){

        var eventDatesAndName = {eventName:$("#inputEventName").val(),
                                 eventStartDate:$("#startDatePicker").val(),
                                 eventEndDate:$("#endDatePicker").val()}
        $.ajax({
          type:"POST",
          url: "/makeRecurringEvents",
          data: eventDatesAndName, //get the startDate, endDate and eventName as a dictionary
          success: function(jsonData){
            var recurringEvents = JSON.parse(jsonData)
            var recurringTable = $("#recurringEventsTable")
            $("#recurringEventsTable tbody tr").remove();

            for (var event of recurringEvents){
              recurringTable.append("<tr><td>"+event.eventName+"</td><td><input name='week"+event.week+"' type='hidden' value='"+event.date+"'>"+event.date+"</td></tr>");
              }
          },
          error: function(error){
            console.log(error)
          }
        });
      }
    });

  $("#checkIsTraining").click(function(){

    if ($("input[name='eventIsTraining']:checked").val() == 'on'){
      $("#checkIsRequired").prop('checked', true);

    }else{
      $("#checkIsRequired").prop('disabled', false);
    }


  });
});

function updateDate(obj) { // updates max and min dates of the datepickers as the other datepicker changes
  var dateToChange = new Date($(obj).val());
  var newMonth = dateToChange.getMonth();
  var newYear = dateToChange.getFullYear();
  if(obj.id == "endDatePicker"){
    var newDay = dateToChange.getDate();
    $("#startDatePicker").datepicker({maxDate: new Date(  newYear, newMonth, newDay)});

    $("#startDatePicker").datepicker("option", "maxDate", new Date(  newYear, newMonth, newDay));
  }
  if(obj.id == "startDatePicker"){
    var newDay = dateToChange.getDate();
    $("#endDatePicker").datepicker({minDate: new Date(  newYear, newMonth, newDay)});
    $("#endDatePicker").datepicker( "option", "minDate", new Date(  newYear, newMonth, newDay));
  }
}
