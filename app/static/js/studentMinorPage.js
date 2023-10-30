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

function showEngagementInformation(row) {
  let username = $("#username").val()
  var type = ""
  let typeID = String(row.id)
  let term = row.name
  if (typeID.startsWith("course")) {
    type = "course"
  } else {
    type = "program"
  }
  console.log(String(term))

  var id = typeID.slice(type.length,typeID.length)
  $.ajax({
    url: `/cceMinor/${username}/getEngagementInformation/${type}/${term}/${id}`,
    type: "GET",
    data: "",
    success: function(response) {
      
    },
    error: function(request, status, error) {
      msgFlash("Error displaying information!", "danger")
    }
});



}