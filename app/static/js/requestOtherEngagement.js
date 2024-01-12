$(document).ready(function(){
    // $("#requestOtherCommEng").on("click", function() {
    //   let username = $("#username").val()
    //   let data = {"username":username}
    //
    //   $.ajax({
    //       url: "/cceMinor/"+username+"/requestOtherCommunityEngagement",
    //       type: "GET",
    //       data: data,
    //       success: alert,
    //       error: function(request, status, error) {
    //         msgFlash("Error saving changes!", "danger")
    //       }
    //   });
    //
    // })
    handleFileSelection("attachmentObject")

    $('#sendOtherRequest').on("click", function(){
      if (!validateForm()) return;
      $('#requestOtherCommEng').attr("action", "/cceMinor/<username>/addCommunityEngagement")
      $('#requestOtherCommEng').submit()
    })
})
