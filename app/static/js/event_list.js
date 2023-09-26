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
          var days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
          var hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
          var minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
          var seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

          var countdownText = days + "d " + hours + "h " + minutes + "m " + seconds + "s";
          $("#countdown-text").text(countdownText);
      } else {
          var countdownText = "now!"
          $("#countdown-text").text(countdownText);
      }
      console.log(countdownText);
  }

  // Set the event date
  var eventDate = new Date($("#countdown").data("event-date")); 
 
  // Initial update
  updateCountdown(eventDate);

  // Update the countdown every second
  setInterval(function() {
      updateCountdown(eventDate);
  }, 1000)

