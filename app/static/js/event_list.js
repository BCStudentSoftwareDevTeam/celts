$(document).ready(function(){
    $("#removeRsvpBtn").click(function(){
        removeRsvpForEvent($("#removeRsvpBtn").val())
    })
    $("#rsvpBtn").click(function(){
        rsvpForEvent($("#rsvpBtn").val())
    })
    $("#toggleButton").on("click", toggleButton)
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

function toggleButton(){
  var toggleButton = document.getElementById("toggleButton");
  var tableRows = document.getElementsByClassName("showlist");

  if (toggleButton.checked) {
    for (var i = 0; i < tableRows.length; i++) {
      var tableRow = tableRows[i];
      if (tableRow.classList.contains("d-none")) {
        tableRow.classList.remove("d-none");
      }
    }
  } else {
    for (var i = 0; i < tableRows.length; i++) {
      var tableRow = tableRows[i];
      if (!tableRow.classList.contains("d-none")) {
        tableRow.classList.add("d-none");
      }
    }
  }
}

