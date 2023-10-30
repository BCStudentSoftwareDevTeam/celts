$(document).ready(function(){
    $("#expressInterest").on("click", function() {
        let username = $("#username").val()
        let data = {"username":username}
        $.ajax({
            url: "/cceMinor/"+username+"/indicateInterest",
            type: "POST",
            data: data,
            success: location.reload(),
            error: function(request, status, error) {
             msgFlash("Error saving changes!", "danger")
           }
      });
    })
})