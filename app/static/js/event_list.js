

function rsvpForEvent(programID, eventID){
  rsvpInfo = {eventId: eventID,
              programId: programID,
              from: 'ajax'}
  console.log(rsvpInfo)

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
