$(document).ready(function(){
    $("#removeRsvpBtn").click(function(){
        removeRsvpForEvent($("#removeRsvpBtn").val())
    })
    $("#rsvpBtn").click(function(){
        rsvpForEvent($("#rsvpBtn").val())
    })
    var viewPastEventsToggle = $("#viewPastEventsToggle");
    viewPastEventsToggle.prop("checked", g_isPastTerm);
    toggleRows(g_isPastTerm);
    viewPastEventsToggle.prop("disabled", g_isPastTerm);    
      
    viewPastEventsToggle.on("change", function(){
      var isChecked = $(this).prop("checked");
      toggleRows(isChecked);

      localStorage.setItem("toggleState", isChecked ? "checked" : "unchecked")
    });

    function toggleRows(isChecked) {
      var tableRows = $(".showlist");
      if (isChecked){
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

// Calculate and update the countdown
function updateCountdown(eventDate) {
  var now = new Date();
  var timeRemaining = eventDate - now;
  

  if (timeRemaining > 0) {
    var days = Math.floor((timeRemaining / (1000 * 60 * 60 * 24))+1);

    var countdownText = '';

    if (days > 1) {
      countdownText = "in " + days + " days";
    } else if (days === 1) {
      countdownText = "is happening tomorrow";
    } 

    $("#countdown-text").text(countdownText);
    if (days = 0) {  
    var countdownText = "is happening today!";
    $("#countdown-text").text(countdownText);
    }
  } else {
    var countdownText = "has already passed";
    $("#countdown-text").text(countdownText);
  }

  console.log(countdownText);
}

// Set the event date from HTML data attribute
var eventDate = new Date($("#countdown").data("event-date"));

// Display the event date in Eastern Time (ET)
var eventDateText = eventDate.toLocaleString('en-US', { timeZone: 'America/New_York' });
$("#event-date").text(eventDateText);

// Initial update
updateCountdown(eventDate);


