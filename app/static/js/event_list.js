$(document).ready(function(){
    $("#removeRsvpBtn").click(function(){
        removeRsvpForEvent($("#removeRsvpBtn").val())
    })
    $("#rsvpBtn").click(function(){
        rsvpForEvent($("#rsvpBtn").val())
    })
    var viewPastEventsToggle = $("#viewPastEventsToggle");
  

    viewPastEventsToggle.prop("checked", false);
    toggleRows(false);  

    // data-isPastTerm="{{(selectedTerm != g.current_term)}}"
    // isPastTerm = viewPastEventsToggle.data("ispastterm");

    viewPastEventsToggle.prop("checked", g_isPastTerm);
    if (g_isPastTerm){
      toggleRows(true)
    }
      

    viewPastEventsToggle.on("change", function(){
      var isChecked = $(this).prop("checked");
      toggleRows(isChecked);

      localStorage.setItem("toggleState", isChecked ? "checked" : "unchecked")
    });

    function toggleRows(isChecked) {
      var tableRows = $(".showlist");
      if (isChecked){
        tableRows.show();
      }
      else{
        tableRows.hide();
      }
    }
})

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



