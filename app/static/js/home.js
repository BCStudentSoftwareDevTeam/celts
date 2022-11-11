$(document).ready(function(){
  $('#descriptionModal').on('show.bs.modal', function (event){
    $("#modalTitle").text('About '+ event.relatedTarget.getAttribute('data-bs-program'))
    $("#modalImage").attr("src", event.relatedTarget.getAttribute('data-bs-image'))
    $('#modalDescription').text(event.relatedTarget.getAttribute('data-bs-description'))
  })
});
