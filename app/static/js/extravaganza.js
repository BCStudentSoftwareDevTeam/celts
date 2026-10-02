$(document).ready(function(){    
    msgFlash();

    $(".interestedInput").click(function updateInterest(){
        var programID = $(this).data("programid");
        var username = $(this).data('username');

        var interest = $(this).is(':checked');
        var routeUrl = interest ? "addInterest" : "removeInterest";
        var interestUrl = "/" + username + "/" + routeUrl + "/" + programID ;
        $.ajax({
            method: "POST",
            url: interestUrl,
            success: function(response) {
                msgFlash("Your program interest selection was saved.", "success", 5000, true);
                window.location.reload();
            },
            error: function(request, status, error) {
                console.log(status,error);
                location.reload();
            }
        });
    });
});
