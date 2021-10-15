

$(document).ready(function(){

  // $("#sendEmail").click(function(){
  //   console.log($("#emailSender").val())
  //   console.log($("#message").val())
  //   // msg = $("#message").val().replace(" ",'%20')
  //   //
  //   // console.log($("#subject").val())
  //   // subject = self.emailInfo['subject'].replace(" ",'%20')
  //
  //   // window.location.href = "mainto:"+$("#emailSender").val()+"?Subject="+$("#subject").val()
  //   window.location.href = "mailto:"+$("#emailSender").val()
  //   // window.location.href = `mailto:${encodeURIComponent(("#emailSender").val())}?subject=+${("#subject").val()}`
  //   // `{encodeURIComponent($("#subject").val())}&body=${encodeURIComponent($("#message").val())}`;
  // })

});

function passEventInfo(eventID, programID, selectedTerm){
  // when the email button for an event is clicked, this passes the eventID and programID to the modal
  $('#emailModal').modal('show')
  $(".modal-body #eventID").val(eventID)
  $(".modal-body #programID").val(programID)
  $(".modal-body #selectedTerm").val(selectedTerm)


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
