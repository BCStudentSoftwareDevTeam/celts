$(document).ready(function(){
  updateIndicatorCounts()

  $("#removeRsvpBtn").click(function(){
      removeRsvpForEvent($("#removeRsvpBtn").val())
  })
  $("#rsvpBtn").click(function(){
      rsvpForEvent($("#rsvpBtn").val())
  })

  var viewPastEventsToggle = $("#viewPastEventsToggle");
  var isChecked = viewPastEventsToggle.prop("checked");
  toggleRows(isChecked);

  viewPastEventsToggle.on("change", function(){
    if (!g_isPastTerm) {
      let isChecked = $(this).prop("checked");
      toggleRows(isChecked);
      // Update server state via AJAX POST
      $.post("/updateToggleState", {
        toggleState: isChecked ? "checked" : "unchecked",
      });
    }
    updateIndicatorCounts();
  });

  function toggleRows(isChecked) {
    console.log(isChecked, " checkstate");
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

//gets number of events in each event list category
function updateIndicatorCounts(){
  $.ajax({
    url: "/eventsList/" + $('#termID').val(),
    type: "GET",
    success: function(EventsCount) {
      const studentLedEventsCount = Number(EventsCount.studentLedEventsCount);
      const trainingEventsCount = Number(EventsCount.trainingEventsCount);
      const bonnerEventsCount = Number(EventsCount.bonnerEventsCount);
      const otherEventsCount = Number(EventsCount.otherEventsCount);
      msgFlash("HELLO", "success"); //REMOVE THESE LATER***********************
      console.log(EventsCount);
      console.log(studentLedEventsCount, trainingEventsCount, bonnerEventsCount, otherEventsCount);

      if (studentLedEventsCount >= 0) {
        $("#studentLedEvents").html(`Student Led Service (${studentLedEventsCount})`);
      }
      if (trainingEventsCount >= 0) {
        $("#trainingEvents").html(`Training and Education (${trainingEventsCount})`);
      }
      if (bonnerEventsCount >= 0) {
        $("#bonnerScholarsEvents").html(`Bonner Scholars (${bonnerEventsCount})`);
      }
      if (otherEventsCount >= 0) {
        $("#otherEvents").html(`Other Events (${otherEventsCount})`);
      }
    },
    error: function(request, status, error) {
      console.log(status,error);
    }
  });
}