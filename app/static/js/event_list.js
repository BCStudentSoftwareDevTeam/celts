$(document).ready(function(){
    $("#removeRsvpBtn").click(function(){
        removeRsvpForEvent($("#removeRsvpBtn").val())
    })
    $("#rsvpBtn").click(function(){
        rsvpForEvent($("#rsvpBtn").val())
    })
    var viewPastEventsToggle = $("#viewPastEventsToggle");
    var isChecked = viewPastEventsToggle.data("initial-state") === "checked";
    viewPastEventsToggle.prop("checked", isChecked);
    toggleRows(isChecked);

    if (!g_isPastTerm) {
      viewPastEventsToggle.on("change", function(){
        isChecked = $(this).prop("checked");
        toggleRows(isChecked);
    
        // Update server state via AJAX POST
        $.post("/updateToggleState", {
          toggleState: isChecked ? "checked" : "unchecked",
        });
    
      });
    } else {
      viewPastEventsToggle.prop("checked", g_isPastTerm);
      toggleRows(g_isPastTerm);
    }

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



