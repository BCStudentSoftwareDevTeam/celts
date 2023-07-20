$(document).ready( function () {

  //make html table to datatable
  var table = $('#SLCProposalTable').DataTable({
   "fnDrawCallback": function(oSettings) {
      if ($('#SLCProposalTable tr').length <= 10) {
         // if entries are less than or equal to 10, there is no need for the dropdown with entries to show.
         $('.dataTables_length').hide();
         //move search box to the left
         $('.dataTables_filter').addClass('float-start');
       }
    }
    

  });

  $('#modalPreview button[data-bs-dismiss="modal"]').click(function () {
    $('#modalPreview').removeClass('show d-block');
  });
   
  $('#modalSubmit').on('hidden.bs.modal', function () {
    $('#addCourseParticipant').val('');
    
  })

  $("#downloadApprovedCoursesBtn").click(function () {
    let termID = $("#downloadApprovedCoursesBtn").val();
    $.ajax({
      url: `/serviceLearning/downloadApprovedCourses/${termID}`,
      type: "GET",
      success: function (response) {
        callback(response);
      },
      error: function (response) {
        console.log(response)
      },


    })
  });
  function removeRsvpForEvent(eventID) {
    removeRsvpInfo = {
      id: eventID,
      from: 'ajax'
    }

    $.ajax({
      url: "/rsvpRemove",
      type: "POST",
      data: removeRsvpInfo,
      success: function (s) {
        location.reload()
      },
      error: function (error, status) {
        console.log(error, status)
      }

    })
  }
});

$("#modalCourseParticipant").on("click", function () {
  $("#modalSubmit").modal("toggle");
});


const fileInput= $("#addCourseParticipant")
fileInput.on('change', handleFileSelect)

function handleFileSelect(event){
  const selectedFile = event.target.files[0];

  if (selectedFile){
    $("#previewButton").prop('disabled', false);
  }
}

$("#cancelModal").click(function(){
  $.ajax({
    url: "/deleteUploadedFile",
    type: 'POST',
    error: function(error, status){
      console.log(error, status)
    }
  });
})