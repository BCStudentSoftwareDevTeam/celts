$(document).ready(function(){
    $("#expressInterest").on("click", function() {
        let username = $("")
        $.ajax({
            url: "",
            type: "POST",
            data: data,
            success: console.log("Successfully updated."),
            error: function(request, status, error) {
             msgFlash("Error saving changes!", "danger")
           }
      });
    })
})