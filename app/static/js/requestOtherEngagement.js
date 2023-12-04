$(document).ready(function(){
    $("#requestOtherCommEng").on("click", function() {
    let username = $("#username").val()
    let data = {"username":username}
    let dataForm = new FormData(this)
    $.ajax({
        url: "/cceMinor/"+username+"/requestOtherCommunityEngagement",
        type: "GET",
        data: dataForm,
        success: alert,
        error: function(request, status, error) {
          msgFlash("Error saving changes!", "danger")
        }
    });
    handleFileSelection("attachmentObject")
  })
})
