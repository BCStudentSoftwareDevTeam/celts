import searchUser from './searchUser.js'

// TODO: empty the courseInstructor input after an instructor has been added to the table.
function callback() {
  let instructor = $("#courseInstructor").val();
  let tableBody = $("#instructorTable").find("tbody");
  let lastRow = tableBody.find("tr:last");
  let newRow = lastRow.clone();
  newRow.find("td:eq(0)").text(instructor);
  newRow.prop("hidden", false);
  lastRow.after(newRow);
}

$("#courseInstructor").on('input', function() {
  searchUser("courseInstructor", callback);
});

$("#instructorTable").on("click", "#remove", function() {
   $(this).closest("tr").remove();
});

let courseInstructors = []
$('#continue').on("click", function() {
  $("#instructorTable tr").each(function(a, b) {
    courseInstructors.push($('.instructorName', b).text());
  });

  $.ajax({
    url: "/courseInstructors",
    data: JSON.stringify(courseInstructors),
    type: "POST",
    contentType: "application/json",
    success: function () {
      $("#slcProposalForm").submit();
    }
  });
});

// -----------------TODO: Rewrite this functionality
// TODO: we need to create a new JS file that is only for saving data in cookies
// and it can be imported elsewhere.
$(document).ready ( function() {
  var cookies = document.cookie;
  if (cookies){
    parsedCookies = JSON.parse(cookies);
    document.cookie = parsedCookies + ";max-age=28800;";

    $("#courseName").val(parsedCookies.courseName);
    $("#courseAbbreviation").val(parsedCookies.courseAbbreviation);
    $("#credit").val(parsedCookies.credit);
    $("#slSectionsToggle").val(parsedCookies.sectionsResponse);
    $("#inputCourseInstructor").val(parsedCookies.inputCourseInstructor);
    $("#slDesignation").val(parsedCookies.slDesignation);
  }

});

function saveSLCdata(){
  var courseName = $('#courseName').val();
  var courseAbbreviation = $('#courseAbbreviation').val()
  var credit = $("#credit").val()
  var slSectionsToggle = $("#slSectionsToggle").val()
  var inputCourseInstructor = $("#inputCourseInstructor").find("option:selected").val();
  var slDesignation = $("#slDesignation").text()

  var proposalData = {
    courseName: courseName,
    courseAbbreviation: courseAbbreviation,
    credit: credit,
    slSectionsToggle: slSectionsToggle,
    inputCourseInstructor: inputCourseInstructor,
    slDesignation: slDesignation
  }

  document.cookie =  JSON.stringify(proposalData) + ";max-age=28800;";
}
