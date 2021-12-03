

function passEventInfo(eventID, programID, selectedTerm){
  // when the email button for an event is clicked, this passes the eventID and programID to the modal
  $('#emailModal').modal('show')
  $(".modal-body #eventID").val(eventID)
  $(".modal-body #programID").val(programID)
  $(".modal-body #selectedTerm").val(selectedTerm)
}


function rsvpForEvent(programID, eventID){
  rsvpInfo = {id: eventID,
              programId: programID,
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

  })
}

function removeRsvpForEvent(programID, eventID){
  removeRsvpInfo = {id: eventID,
              programId: programID,
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
