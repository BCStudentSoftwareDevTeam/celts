$(document).ready(function() {
    console.log("yo")
    $.ajax({
        url: "/cceMinor/getInterestedStudents",
        type: "GET",
        data: "",
        success: function(count) {
          console.log(interestedStudentsCount)
          if (Number(interestedStudentsCount) > 0) {
            let minorManagement = $("#minorManagement").html()
            $("#minorManagement").html(`${minorManagement} (${count})`)
          } 
      },
        error: function(request, status, error) {
          console.log(status,error);
        }
      })
});