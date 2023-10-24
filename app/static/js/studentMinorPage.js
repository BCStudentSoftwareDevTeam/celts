$(document).ready(function(){
    $("#expressInterest").on("click", function() {
        let username = $("#username").val()
        let data = {"username":username}
        $.ajax({
            url: "/profile/"+username+"/cceMinor",
            type: "POST",
            data: data,
            success: console.log("Successfully updated."),
            error: function(request, status, error) {
             msgFlash("Error saving changes!", "danger")
           }
      });
    })
})