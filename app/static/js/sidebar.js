$(document).ready(function() {
    // add hovers to describe what the numbers we are adding to the sidebar mean.
    $(".courseManagement").popover({
      trigger: "hover",
      sanitize: false,
      html: true,
      content: function() {
        return "Amount of pending course proposals for the current term."
      }
    });
    $(".minorManagement").popover({
      trigger: "hover",
      sanitize: false,
      html: true,
      content: function() {
          return "Amount of students who have expressed interest in the minor."
      }
    });

    // fetch the number of interested students and unapproved courses and display them in the sidebar if there are any
    $.ajax({
      url: "/admin/getSidebarInformation",
      type: "GET",
      success: function(sidebarInformation) {
        const unapprovedCoursesCount = Number(sidebarInformation.unapprovedCoursesCount)
        const interestedStudentsCount = Number(sidebarInformation.interestedStudentsCount)
        if (unapprovedCoursesCount > 0) {
          $("#courseManagement").html(`Course Management (${unapprovedCoursesCount})`)
        } 
        if (interestedStudentsCount > 0) {
          $("#minorManagement").html(`Minor Management (${interestedStudentsCount})`)
        }
        if (interestedStudentsCount + unapprovedCoursesCount > 0) {
          $("#admin").html(`Admin (${interestedStudentsCount + unapprovedCoursesCount})`)
        }
      },
      error: function(request, status, error) {
        console.log(status,error);
      }
    })
});