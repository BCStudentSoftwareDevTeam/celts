
$( document ).ready(function() {
  //force-hide all modals when user clicks outisde the modal or clicks the x
  $('.modal').on('hidden.bs.modal', function () {
    $('.modal').modal('hide')
  });
});

function passEventInfo(eventID, programID){
  // when the email button for an event is clicked, this passes the eventID and programID to the modal
  $('.modal').modal('show')
  $(".modal-body #eventID").val(eventID)
  $(".modal-body #programID").val(programID)
}

function rsvpForEvent(programID, eventID){
  rsvpInfo = {eventId: eventID,
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
  removeRsvpInfo = {eventId: eventID,
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
