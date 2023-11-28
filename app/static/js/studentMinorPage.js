$(document).ready(function(){
    $("#expressInterest").on("click", function() {
      let username = $("#username").val()
      let data = {"username":username}
      $.ajax({
          url: "/cceMinor/"+username+"/indicateInterest",
          type: "POST",
          data: data,
          success: function(s) {
            console.log(s)

            location.reload()
          },
          error: function(request, status, error) {
            console.log(error)
            msgFlash("Error saving changes!", "danger")
          }
      });
    })

    
})

function showEngagementInformation(row) {
  // get the row object that was clicked on and parse it for the necessary values
  let username = $("#username").val()
  var type = ""
  let typeID = String(row.id)
  let term = row.name

  // determine what the type of engagement we are looking at is
  if (typeID.startsWith("course")) {
    type = "course"
  } else {
    type = "program"
  }

  // based on how long the type is, get the remaining characters afterwards that represent the id
  var id = typeID.slice(type.length,typeID.length)
  $.ajax({
    url: `/cceMinor/${username}/getEngagementInformation/${type}/${term}/${id}`,
    type: "GET",
    data: "",
    success: function(response) {
      // create the list that will store the html
      // will be joined later to make a string
      var html = [] 
      html.push("<div>")
      if (type == "program") {
        let program = response["program"]
        let events = response["events"]

        html.push(`<h4>${program} History</h4>`)
        html.push("<ul>")

        // add a list element to the html for each event in our list of events
        // link to the event view page as well
        for (let i = 0; i < events.length; i++) {
          html.push(`<li><a href="/event/${events[i]["id"]}/view">${events[i]["name"]}</a></li>`)
        }

        html.push("</ul>")
      } else {
        let course = response["course"]
        let instructors = response["instructors"]

        // add important fields to display
        html.push(`<h4>${course["courseName"]} Information</h4>`)
        html.push(`<p><b>Instructors:</b> ${instructors.join(", ")}</p>`)
        html.push(`<p><b>Section Designation:</b> ${course["sectionDesignation"]}</p>`)
        html.push(`<p><b>Course Credit:</b> ${course["courseCredit"]}</p>`)
        html.push(`<p><b>SLC Component:</b> ${Boolean(course["hasSlcComponent"]) ? "Yes" : "No"}</p>`)
      }
      html.push("</div>")

      // modify the displayed html by joining together the list we have been pushing to
      $(`#set${term}`).html(html.join(""))
    },
    error: function(request, status, error) {
      msgFlash("Error displaying information!", "danger")
    }
});



}