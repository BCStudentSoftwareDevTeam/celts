$(document).ready(function() {
    $.ajax({
        url: "admin/getInterestedStudents/",
        type: "GET",
        contentType: "application/json",
        dataType: "json",
        success: function(count) {
          if (Number(count) > 0) {
            let minorManagement = $("#minorManagement").html()
            $("#minorManagement").html(`${minorManagement} (${count})`)
          } 
      },
        error: function(request, status, error) {
          console.log(status,error);
        }
      })
}