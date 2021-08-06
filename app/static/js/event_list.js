

function rsvpForEvent(programID, eventID){
  rsvpInfo = {eventId: eventID,
              programId: programID,
              from: 'ajax'}

  $.ajax({
    url: "/rsvpForEvent",
    type: "POST",
    data: rsvpInfo,
    success: function(s){
        location.reload() // ?????????????????????????????????????
    },
    error: function(error, status){
        console.log(error, status)
    }

  })
}

function rsvpForEvent(programID, eventID){
  removeRsvpInfo = {eventId: eventID,
              programId: programID,
              from: 'ajax'}

  $.ajax({
    url: "/rsvpRemove",
    type: "POST",
    data: removeRsvpInfo,
    success: function(s){
        location.reload() // ?????????????????????????????????????
    },
    error: function(error, status){
        console.log(error, status)
    }

  })
}
