import { searchUser } from '/app/static/js/searchStudent.js'

$(document).ready ( function() {
  var cookies = document.cookie;
  console.log("is there cookie?", document.cookie);
  if (cookies){
    console.log("cookie");
    parsedCookies = JSON.parse(cookies);
    document.cookie = parsedCookies + ";max-age=28800;";
    console.log("par", parsedCookies.sectionsResponse);

    $("#courseName").val(parsedCookies.courseName);
    $("#courseAbbreviation").val(parsedCookies.courseAbbreviation);
    $("#credit").val(parsedCookies.credit);
    $("#slSectionsToggle").val(parsedCookies.sectionsResponse);
    $("#inputCourseInstructor").val(parsedCookies.inputCourseInstructor);
    $("#slDesignation").val(parsedCookies.slDesignation);
  }

  searchUser();

});
function saveSLCdata(){
  // courseInstructor = $()
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
  console.log(proposalData, "data");

  document.cookie =  JSON.stringify(proposalData) + ";max-age=28800;";
}
function searchInstructor(){
var query = $("#instructorInput").val()
$("#instructorInput").autocomplete({
  minLength: 2,
  source: function(request, response){
    $.ajax({
      url: "/searchInstructor/" + query,
      type: "GET",
      contentType: "application/json",
      data: query,
      dataType: "json",
      success: function(dictToJSON) {
        response($.map( dictToJSON, function( item ) {
          return {
            label: item,
            value: dictToJSON[item]
        }
      }))
    },
      error: function(request, status, error) {
        console.log(status,error);
      }
    })
  },
  select: function( event, ui ) {
    var instructorName = ui.item.value
    $("#instructorTable").append('<tr><td>' + instructorName + '</td><td><button id="removeButton" onclick="removeRow(this)" type="button"><i class="bi bi-trash" style="font-size:20px"></i></button></td></tr>');
    $("#instructorInput").val(''); return false;

    }
  });
};


function removeRow(e) {
  $(e).parent().parent().remove();
}
