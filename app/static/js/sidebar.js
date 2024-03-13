$(document).ready(function() {
    $.ajax({
        url: "/admin/getInterestedStudentsCount",
        type: "GET",
        data: "",
        success: function(interestedStudentsCount) {
          if (Number(interestedStudentsCount) > 0) {
            $("#minorManagement").html(`Minor Management (${interestedStudentsCount})`)
          } 
      },
        error: function(request, status, error) {
          console.log(status,error);
        }
      })
      $.ajax({
        url: "/admin/getUnapprovedCoursesCount",
        type: "GET",
        data: "",
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