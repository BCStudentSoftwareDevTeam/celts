$(document).ready(function() {
    // fetch the number of interested students and display them  in the sidebar if there are any
    $.ajax({
        url: "/admin/getInterestedStudentsCount",
        type: "GET",
        success: function(interestedStudentsCount) {
          if (Number(interestedStudentsCount) > 0) {
            $("#minorManagement").html(`Minor Management (${interestedStudentsCount})`)
          } 
      },
      error: function(request, status, error) {
        console.log(status,error);
      }
    })
    // fetch the number of unapproved courses and display in the sidebar them if there are any
    $.ajax({
      url: "/admin/getUnapprovedCoursesCount",
      type: "GET",
      success: function(unapprovedCoursesCount) {
        if (Number(unapprovedCoursesCount) > 0) {
          $("#courseManagement").html(`Course Management (${unapprovedCoursesCount})`)
        } 
      },
      error: function(request, status, error) {
        console.log(status,error);
      }
    })

});