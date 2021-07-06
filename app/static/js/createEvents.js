
$(document).ready(function(){

  $(".readonly").on('keydown paste', function(e){ //makes the input fields act like readonly (readonly doesn't work with required)
        if(e.keyCode != 9) // ignore tab
            e.preventDefault();
    });

  $.datepicker.setDefaults({
    dateFormat:'yy-mm-dd'
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
    var newDay = dateToChange.getDate() + 1;
    $("#startDatePicker").datepicker({maxDate: new Date(newYear, newMonth, newDay)});
    $("#startDatePicker").datepicker("option", "maxDate", new Date(newYear, newMonth, newDay));
  }
  if(obj.id == "startDatePicker"){
    if($('input[name="recurringEvent"]:checked').val() == 'true'){ //recurring event shouldn't have same start and end date
      var newDay = dateToChange.getDate() + 2;
    }else{
    var newDay = dateToChange.getDate() + 1;
    }
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
