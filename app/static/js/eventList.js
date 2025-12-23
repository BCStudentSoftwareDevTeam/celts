$(document).ready(function(){

  $("#removeRsvpBtn").click(function(){
      removeRsvpForEvent($("#removeRsvpBtn").val())
  })
  $("#rsvpBtn").click(function(){
      rsvpForEvent($("#rsvpBtn").val())
  })
  //ensure that toggle state is consistent across terms
  if (!g_isPastTerm) {
    var toggleState = sessionStorage.getItem('toggleState') || 'unchecked';
    var viewPastEventsToggle = $("#viewPastEventsToggle");
    viewPastEventsToggle.prop('checked', toggleState === 'checked');

  } else {
    var viewPastEventsToggle = $("#viewPastEventsToggle");
    viewPastEventsToggle.prop('checked', true);
  }
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
      $(".no-upcoming").hide()
    } else {
      tableRows.hide();
      $(".no-upcoming").show()
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
      const volunteerOpportunitiesCount = Number(eventsCount.volunteerOpportunitiesCount);
      const upcomingVolunteerCount = Number(eventsCount.countUpcomingVolunteerOpportunitiesCount);
      const pastVolunteerCount = Number(eventsCount.countPastVolunteerOpportunitiesCount);
      const trainingEventsCount = Number(eventsCount.trainingEventsCount);
      const engagementEventsCount = Number(eventsCount.engagementEventsCount);
      const bonnerEventsCount = Number(eventsCount.bonnerEventsCount);
      const celtsLaborCount = Number(eventsCount.celtsLaborCount);
      const toggleStatus = eventsCount.toggleStatus;
      
      $("#viewPastEventsToggle").prop(toggleStatus, true);

      // use ternary operators to populate the tab with a number if there are events, and clear the count if there are none

      if (toggleStatus === "checked") {
        // Toggle ON → show total (upcoming + past)
        if (volunteerOpportunitiesCount > 0) {
          $("#volunteerOpportunities").html(
            `Volunteer Opportunities (${volunteerOpportunitiesCount})`
          );
        } else {
          $("#volunteerOpportunities").html(`Volunteer Opportunities`);
        }
      } else {
        // Toggle OFF → show upcoming only
        if (upcomingVolunteerCount > 0) {
          $("#volunteerOpportunities").html(
            `Volunteer Opportunities (${upcomingVolunteerCount})`
          );
        } else {
          $("#volunteerOpportunities").html(`Volunteer Opportunities`);
        }
      }
      trainingEventsCount > 0 ? $("#trainingEvents").html(`Trainings (${trainingEventsCount})`) : $("#trainingEvents").html(`Trainings`)
      engagementEventsCount > 0 ? $("#engagementEvents").html(`Education and Engagement (${engagementEventsCount})`) : $("#engagementEvents").html('Education and Engagement')
      bonnerEventsCount > 0 ? $("#bonnerScholarsEvents").html(`Bonner Scholars (${bonnerEventsCount})`) : $("#bonnerScholarsEvents").html(`Bonner Scholars`)
      celtsLaborCount > 0 ? $("#celtsLabor").html(`Celts Labor (${celtsLaborCount})`) : $("#celtsLabor").html(`Celts Labor`)
    },
    error: function(request, status, error) {
      console.log(status,error);
    }
  });
}
