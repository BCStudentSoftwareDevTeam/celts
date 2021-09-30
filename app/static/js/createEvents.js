//
// updates max and min dates of the datepickers as the other datepicker changes
function updateDate(obj) { 
  var dateToChange = new Date($(obj).val());
  var newMonth = dateToChange.getMonth();
  var newYear = dateToChange.getFullYear();
  var newDay = dateToChange.getDate();

  if(obj.id == "startDatePicker") {
    $("#endDatePicker").datepicker({minDate: new Date(  newYear, newMonth, newDay)});
    $("#endDatePicker").datepicker( "option", "minDate", new Date(  newYear, newMonth, newDay));
  }

  if (obj.id == "endDatePicker") {
    $("#startDatePicker").datepicker({maxDate: new Date(  newYear, newMonth, newDay)});
    $("#startDatePicker").datepicker("option", "maxDate", new Date(  newYear, newMonth, newDay));
  }
}

/*
 * Run when the webpage is ready for javascript
 */
$(document).ready(function(){

  $("#checkIsRecurring").click(function() {
    var recurringStatus = $("input[name='isRecurring']:checked").val()
    if (recurringStatus == 'on') {
      $("#endDateStyle, #recurringTableDiv").removeClass('d-none')
      $("#endDatePicker").prop('required', true);
    } else {
      $("#endDateStyle, #recurringTableDiv").addClass('d-none')
      $("#endDatePicker").prop('required', false);
    }
  });

$(document).ready(function(){
  if($(".datePicker").is("readonly")){
    $( ".datePicker" ).datepicker( "option", "disabled", true );
}

});
  //makes the input fields act like readonly (readonly doesn't work with required)
  $(".readonly").on('keydown paste', function(e){ 
        if(e.keyCode != 9) // ignore tab
            e.preventDefault();
    });

  $.datepicker.setDefaults({
    minDate:  new Date($.now()),
    dateFormat:'mm-dd-yy'
  });

  $("#startDate").click(function() {
    $("#startDatePicker").datepicker().datepicker("show"); 
  });

  $("#endDate").click(function() {
    $("#endDatePicker").datepicker().datepicker("show"); 
  });

    $("#startDatePicker, #endDatePicker").change(function(){

      if ( $("#startDatePicker").val() && $("#endDatePicker").val()){

        var eventDatesAndName = {name:$("#inputEventName").val(),
                                 isRecurring: true,
                                 startDate:$("#startDatePicker").val(),
                                 endDate:$("#endDatePicker").val()}
        $.ajax({
          type:"POST",
          url: "/makeRecurringEvents",
          data: eventDatesAndName, //get the startDate, endDate and name as a dictionary
          success: function(jsonData){
            var recurringEvents = JSON.parse(jsonData)
            var recurringTable = $("#recurringEventsTable")
            $("#recurringEventsTable tbody tr").remove();

            for (var event of recurringEvents){
              recurringTable.append("<tr><td>"+event.name+"</td><td><input name='week"+event.week+"' type='hidden' value='"+event.date+"'>"+event.date+"</td></tr>");
              }
          },
          error: function(error){
            console.log(error)
          }
        });
      }
    });

  $("#checkIsTraining").click(function(){

    if ($("input[name='isTraining']:checked").val() == 'on'){
      $("#checkIsRequired").prop('checked', true);

    }else{
      $("#checkIsRequired").prop('disabled', false);
    }


  });
});
