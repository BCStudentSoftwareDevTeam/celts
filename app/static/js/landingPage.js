$(document).ready(function(){
    $('#descriptionModal').on('show.bs.modal', function(event){
    $("#modalTitle").text('About '+ event.relatedTarget.getAttribute('data-bs-program'))
    $("#modalImage").attr("src", event.relatedTarget.getAttribute('data-bs-image'))
    $('#modalDescription').text(event.relatedTarget.getAttribute('data-bs-description'))
    $('#modalProgram').data('program_id', event.relatedTarget.getAttribute('data-bs-id'))
  })
  $('.eventsListButton').on('click', function(){
    let term = $(this).data("term")
    let programID = $(this).data("program_id")
    $.ajax({
      url:  "/goToEventsList/"+programID,
      type: "GET",
      success: function(response) {
        if (response.activeTab === "studentLedEvents"){
          window.location.href += "eventsList/"+term+"/"+response.activeTab+"/"+programID
        } else {
          window.location.href += "eventsList/"+term+"/"+response.activeTab
        }
      }
    });
  })
});
