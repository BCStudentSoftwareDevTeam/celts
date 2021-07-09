
$(document).ready(function(){

  $(".readonly").on('keydown paste', function(e){ //makes the input fields act like readonly (readonly doesn't work with required)
        if(e.keyCode != 9) // ignore tab
            e.preventDefault();
    });

  $.datepicker.setDefaults({
    dateFormat:'mm-dd-yy'
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
