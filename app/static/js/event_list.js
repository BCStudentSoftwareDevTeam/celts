$(document).ready(function(){
    $("#removeRsvpBtn").click(function(){
        removeRsvpForEvent($("#removeRsvpBtn").val())
    })
    $("#rsvpBtn").click(function(){
        rsvpForEvent($("#rsvpBtn").val())
    })
    $("#toggleButton").on("click", toggleButton)
    localStorage.removeItem("toggleState");
    var toggleButton = $("#toggleButton");
    toggleButton.prop("checked", false);
    toggleRows(false)

    toggleButton.on("change", function(){
      var isChecked = $(this).prop("checked");
      toggleRows(isChecked)

      localStorage.setItem("toggleState", isChecked ? "checked" : "unchecked")
    });
    function toggleRows(isChecked) {
      var tableRows = $(".showlist");
      console.log("list has been accessed")
      if (isChecked){
        tableRows.show();
        console.log("table list is displayed")
      }
      else{
        tableRows.hide();
        console.log("table list is hidden")
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



