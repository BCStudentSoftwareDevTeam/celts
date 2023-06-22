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

function addCourseFile(addCourseParticipant) {
  var addCourseFileInfo = {
    id: addCourseParticipant,
    from: 'ajax'
  };

  $.ajax({
    url: "/uploadCourseParticipantFile",
    type: "POST",
    data: addCourseFileInfo,
    success: function (response) {
      saveFileToDatabase(response.filePath);
      location.reload();
    },
    error: function (error, status) {
      console.log(error, status);
    }
  });
}

function saveFileToDatabase(filePath) {
  // Code to save the file path in the database
  // We can may be replace this with our actual database-saving logic after testing if it actually print in console 
  console.log("Saving file to database:", filePath);
}


