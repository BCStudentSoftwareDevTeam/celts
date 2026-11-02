$(document).ready(function(){

    $(".interestedInput").click(function updateInterest(){
        var checkbox = $(this);
        var programID = checkbox.data("programid");
        var username = checkbox.data('username');
        var programName = checkbox.closest("tr").find("#programNameTable").text().trim();

        var interest = checkbox.is(':checked');
        var routeUrl = interest ? "addInterest" : "removeInterest";
        var interestUrl = "/" + username + "/" + routeUrl + "/" + programID + "/False";
        checkbox.prop("disabled", true);
        $.ajax({
            method: "POST",
            url: interestUrl,
            success: function(response) {
                var message = interest ? "Your interest in " + programName + " was saved!"
                                       : programName + " was removed from your interests.";
                showInterestFlash(message, "success");
            },
            error: function(request, status, error) {
                console.log(status,error);
                checkbox.prop("checked", !interest);
                showInterestFlash("Something went wrong updating " + programName + ". Please try again.", "danger");
            },
            complete: function() {
                checkbox.prop("disabled", false);
            }
        });
    });
});

function showInterestFlash(message, status) {
    var icon = status == "success" ? "bi-check-circle-fill" : "bi-exclamation-triangle-fill";
    var alert = $(`<div class="alert alert-${status} extravaganza-flash shadow d-flex align-items-center mb-2" role="alert">
                     <span class="bi ${icon} me-2 flex-shrink-0"></span>
                     <span class="flex-grow-1"></span>
                     <button type="button" class="btn-close ms-2" aria-label="Close"></button>
                   </div>`);
    alert.find(".flex-grow-1").text(message);
    alert.find(".btn-close").click(() => alert.remove());

    $("#extravaganzaFlashContainer").empty().append(alert);
    alert.delay(3000).fadeOut(400, () => alert.remove());
}
