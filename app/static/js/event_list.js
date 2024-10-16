$(document).ready(function(){

  $("#removeRsvpBtn").click(function(){
      removeRsvpForEvent($("#removeRsvpBtn").val())
  })
  $("#rsvpBtn").click(function(){
      rsvpForEvent($("#rsvpBtn").val())
  })
  //ensure that toggle state is consistent across terms
  var toggleState = sessionStorage.getItem('toggleState') || 'unchecked';
  var viewPastEventsToggle = $("#viewPastEventsToggle");
  viewPastEventsToggle.prop('checked', toggleState === 'checked');
  var isChecked = viewPastEventsToggle.prop("checked");
  toggleRows(isChecked);
  
  updateIndicatorCounts(isChecked)
  //update indicator numbers when toggle is changed
  viewPastEventsToggle.on("change", function(){
    if (!g_isPastTerm) {
      let isChecked = $(this).prop("checked");
      toggleRows(isChecked);
      updateIndicatorCounts(isChecked);
      sessionStorage.setItem('toggleState', isChecked ? "checked" : "unchecked");
    }
  });

  function toggleRows(isChecked) {
    var tableRows = $(".showlist");
    if (isChecked) {
      tableRows.show();
    } else {
      tableRows.hide();
    }
  }
});

function rsvpForEvent(eventID){
  rsvpInfo = {id: eventID,
              from: 'ajax'}

  $.ajax({
    url: "/rsvpForEvent",
    type: "POST",
    data: rsvpInfo,
    success: function(s){
        location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }
  });
}

function removeRsvpForEvent(eventID){
  removeRsvpInfo = {id: eventID,
                    from: 'ajax'}

  $.ajax({
    url: "/rsvpRemove",
    type: "POST",
    data: removeRsvpInfo,
    success: function(s){
        location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }
  })
}

//gets number indicator of events in each event list category
function updateIndicatorCounts(isChecked){
  $.ajax({
    url: "/eventsList/" + $('#termID').val(),
    type: "GET",
    data: {
      toggleState: isChecked ? "checked" : "unchecked",
    },
    success: function(eventsCount) {
      const studentLedEventsCount = Number(eventsCount.studentLedEventsCount);
      const trainingEventsCount = Number(eventsCount.trainingEventsCount);
      const bonnerEventsCount = Number(eventsCount.bonnerEventsCount);
      const otherEventsCount = Number(eventsCount.otherEventsCount);
      const toggleStatus = eventsCount.toggleStatus;
      
      $("#viewPastEventsToggle").prop(toggleStatus, true);

      // use ternary operators to populate the tab with a number if there are events, and clear the count if there are none
      studentLedEventsCount > 0 ? $("#studentLedEvents").html(`Student Led Service (${studentLedEventsCount})`) : $("#studentLedEvents").html(`Student Led Service`)
      trainingEventsCount > 0 ? $("#trainingEvents").html(`Training and Education (${trainingEventsCount})`) : $("#trainingEvents").html(`Training and Education`)
      bonnerEventsCount > 0 ? $("#bonnerScholarsEvents").html(`Bonner Scholars (${bonnerEventsCount})`) : $("#bonnerScholarsEvents").html(`Bonner Scholars`)
      otherEventsCount > 0 ? $("#otherEvents").html(`Other Events (${otherEventsCount})`) : $("#otherEvents").html(`Other Events`)
    },
    error: function(request, status, error) {
      console.log(status,error);
    }
  });
}
