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

    if (!g_isPastTerm) {
      viewPastEventsToggle.on("change", function(){
        let isChecked = $(this).prop("checked");
        toggleRows(isChecked);
    
        // Update server state via AJAX POST
        $.post("/updateToggleState", {
          toggleState: isChecked ? "checked" : "unchecked",
        });
    
      });
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

// function undoButton(){
//   undoButton = {from: 'ajax'}
//   $.ajax({
//     url: "/event/undo",
//     type: "POST",
//     data: undoButton,
//     success: function(){
//       alert("Successfully undone!")
//     },
//     error: function(error, status){
//       console.log(error, status)
//     }
//   })
// }
