$(document).ready(function(){
    $("#removeRsvpBtn").click(function(){
        removeRsvpForEvent($("#removeRsvpBtn").val())
    })
    $("#rsvpBtn").click(function(){
        rsvpForEvent($("#rsvpBtn").val())
    })
   var storedToggleState = localStorage.getItem("toggleState");
  var isChecked = storedToggleState === "checked";
  // Initialize toggle based on retrieved state
  var viewPastEventsToggle = $("#viewPastEventsToggle");
  viewPastEventsToggle.prop("checked", isChecked);
  toggleRows(isChecked);
  // Handle toggle change
  viewPastEventsToggle.on("change", function() {
    isChecked = $(this).prop("checked");
    toggleRows(isChecked);
    // Update localStorage with new toggle state
    localStorage.setItem("toggleState", isChecked ? "checked" : "unchecked");
  });
  // Function to toggle rows visibility
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



