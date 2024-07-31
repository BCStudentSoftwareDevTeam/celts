$(document).ready(function(){

  $("#removeRsvpBtn").click(function(){
      removeRsvpForEvent($("#removeRsvpBtn").val())
  })
  $("#rsvpBtn").click(function(){
      rsvpForEvent($("#rsvpBtn").val())
  })

  var viewPastEventsToggle = $("#viewPastEventsToggle");
  var isChecked = viewPastEventsToggle.prop("checked");
  toggleRows(isChecked);

  //updateIndicatorCounts(isChecked)

  viewPastEventsToggle.on("change", function(){
    if (!g_isPastTerm) {
      let isChecked = $(this).prop("checked");
      toggleRows(isChecked);
    }
    // $.post("/updateToggleState", {
    //   toggleState: isChecked ? "checked" : "unchecked"
    // })
  });

  function toggleRows(isChecked) {
    console.log(isChecked, " checkstate");
    var tableRows = $(".showlist");
    if (isChecked) {
      tableRows.show();
    } else {
      tableRows.hide();
    }
    updateIndicatorCounts(isChecked);
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
      const toggle_state = eventsCount.toggle_state;
      msgFlash("HELLO", "success"); //REMOVE THESE LATER***********************
      console.log(eventsCount);
      console.log(studentLedEventsCount, trainingEventsCount, bonnerEventsCount, otherEventsCount);

      $("#viewPastEventsToggle").prop('checked', toggle_state === 'checked');

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