$(document).ready(function(){

    $(".interestedInput").click(function updateInterest(){
        var checkbox = $(this);
        var programID = checkbox.data("programid");
        var username = checkbox.data('username');
        var programName = checkbox.closest("tr").find("#programNameTable").text().trim();

        var interest = checkbox.is(':checked');
        var routeUrl = interest ? "addInterest" : "removeInterest";
        var interestUrl = "/" + username + "/" + routeUrl + "/" + programID;
        checkbox.prop("disabled", true);
        $.ajax({
            method: "POST",
            url: interestUrl,
            data: { showFlash: false },
            success: function(response) {
                var message = interest ? "Your interest in " + programName + " was saved!"
                                       : programName + " was removed from your interests.";
                msgFlash(message, "success");
            },
            error: function(request, status, error) {
                console.log(status,error);
                checkbox.prop("checked", !interest);
                msgFlash("Something went wrong updating " + programName + ". Please try again.", "danger");
            },
            complete: function() {
                checkbox.prop("disabled", false);
            }
        });
    });
});

