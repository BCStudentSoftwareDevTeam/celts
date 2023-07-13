$(document).ready( function () {

  //make html table to datatable
   var table =  $('#myTable').DataTable({
   "fnDrawCallback": function(oSettings) {
     if ($('#myTable tr').length <= 10) {
         // if entries are less than or equal to 10, there is no need for the dropdown with entries to show.
         $('.dataTables_length').hide();
         //move search box to the left
         $('.dataTables_filter').addClass('float-start');
       }
    }
  });
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
    console.log("My file has been selected", selectedFile.name);
    $("#previewButton").prop('disabled', false);
  }
}


  // $("#previewButton").on("click", function(){
  //   console.log("Preview is here, ourrrrrrrrrrrrrrrrrrrrrrra")
  //   $("#modalPreview").modal("toggle");
  //   // $("#modalPreview").preventDefault();
  //   });


// $("#previewButton").on("click", function () {
//   $("#modalPreview").modal("toggle");
// });


// $(document).ready(function(){
//   $("#previewButton").click(function(){
//     $("#modalPreview").addClass('show d-block');
//   })
// })





$(document).ready(function(){
  $('.btn-secondary[data-bs-dismiss="modal"]').click(function(){
    location.reload();
  })
  })










