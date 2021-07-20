$('.accordion-button').on('click', (evt) => {
    $(this).hide(); // does not run a DOM query
    $('.accordion-collapse').hide() // runs a DOM query
});

function addTableData(eventName, eventDate, eventTime, eventLocation) {
  // currentEvent = $("#event").val()
  // console.log(currentEvent)
  // console.log(currentEvent.program.programName)
  var table = $("#accordionTable"+event.program)
  // // console.log(event.program)
  // // console.log(table)
  table.append("<tr><td>"+eventName+"</td><td>"+eventDate+"</td><td>"+eventDate+"</td><td>"+eventTime+"</td><td>"+eventLocation+"</td></tr>");
}
