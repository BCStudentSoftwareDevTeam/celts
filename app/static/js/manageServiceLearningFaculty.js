$(document).ready( function () {

  /******** Faculty Table Management **************/
  var table = $('#SLCFacultyTable').DataTable({
   "fnDrawCallback": function(oSettings) {
      $('.dataTables_length').hide();
      $('.dataTables_filter').addClass('float-none');
    }
  });
  const instructorCheckboxes = $(".instructorCheckbox");

  $("#emailSelectedButton").on("click", function () {
    const selectedEmails = Array.from(instructorCheckboxes)
                                .filter((checkbox) => checkbox.checked)
                                .map((checkbox) => checkbox.getAttribute("data-email"))
                                .join(";");

    if (selectedEmails.length) {
      const windowRef = window.open(`mailto:${selectedEmails}?subject=Renew Course Proposal`, '_blank');
      windowRef.focus();

      setTimeout(function(){
        if(!windowRef.document) {
            windowRef.close();
        }
      }, 500);
    }
  });

  const selectAll = $("#selectAllOthersButton");
  selectAll.on("click", function () {
    let selecting = (selectAll.text() == "Select All");
    instructorCheckboxes.each(function(i,box) {
        box.checked = selecting
    })
    selectAll.text(selecting ? "Unselect All" : "Select All");
  });
  

  /******** Preview Events **************/
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

  /******** Course Participant Stuff **************/
    $("#modalCourseParticipant").on("click", function () {
      $("#modalSubmit").modal("toggle");
    });

    $('#closeAddCourseParticipants').on('click', function () {
      $('#addCourseParticipants')[0].form.reset()
      $('#previewButton').prop('disabled', true)
    })

    const fileInput= $("#addCourseParticipants")
    fileInput.on('change', handleFileSelect)

    function handleFileSelect(event){
      const selectedFile = event.target.files[0];

      if (selectedFile){
        $("#previewButton").prop('disabled', false);
      }
    }

    $("#cancelModalPreview").click(function(){
      $.ajax({
        url: "/deleteUploadedFile",
        type: 'POST',
        error: function(error, status){
          console.log(error, status)
        }
      });
    })

    $("a.studentview").click(function(e) {
        let course_id=e.target.getAttribute('data-course');
        if(e.target.innerHTML == "View") {
            $(`#${course_id}_students`).show();
            e.target.innerHTML = "Hide"; 
        } else {
            $(`#${course_id}_students`).hide();
            e.target.innerHTML = "View"; 
        }
    });
});

