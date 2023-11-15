$(document).ready(function(){
    $("#requestOtherCommEng").on("click", function() {
    let username = $("#username").val()
    let data = {"username":username}
    $.ajax({
        url: "/cceMinor/"+username+"/requestOtherCommunityEngagement",
        type: "POST",
        data: data,
        success: location.reload(),
        error: function(request, status, error) {
          msgFlash("Error saving changes!", "danger")
        }
    });
  })
})
