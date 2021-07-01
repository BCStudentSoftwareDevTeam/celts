$(document).ready(function(){
  $(".Volunteers").hide();
  $(".outsidepart").hide();
  $("#Outsearch").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#Partul a").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      if(!value) {
        $(".outsidepart").hide();
      }
      });
    });
  $("#Volsearch").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#Volul a").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      if(!value) {
        $(".Volunteers").hide();
      }
    });
  });
});

function addVolunteer(e){
  volunteersName = $(e).text()
  $("#Volunteertable").append('<tr><td>' + volunteersName + '</td><td><button id="removeButton" onclick="removeVolunteer(this)" type="button">x</button></td></tr>')
  console.log(volunteersName)

}
function removeParticipants(e) {
  // var $row = $(e);
  //console.log($row.find(':nth-child(2)').text());
  // console.log($(e).parent().parent()[0].(document).text("td:nth-child(2)"));
  text = $(e).parent().parent()[0].textContent;
  text2 = JSON.stringify(text);
  // console.log(text2);
  $.ajax({
    method: "POST",
    url: "/removeParticipant",
    data: text2,
    contentType: "application/json; charset=utf-8",
    success: function(response) {
      console.log("Success");
    },
    error: function(request, status, error) {
      console.log(status,error);
    }
  });
  $(e).parent().parent().remove();
}

function removeVolunteer(e) {
  $(e).parent().parent().remove();
}

// function textboxValue() {
//   var formValues = {
//       event: "2",
//       firstName: $("#firstNameTextarea").val(),
//       lastName: $("#lastNameTextarea").val(),
//       emailEntry: $("#emailTextarea").val(),
//       phoneNumber: $("#phoneNumberTextarea").val(),
//     };
//   var formStringified = JSON.stringify(formValues, null, 2);
//   $.ajax({
//     method: "POST",
//     url: "/createParticipant",
//     data: formStringified,
//     contentType: "application/json; charset=utf-8",
//     success: function(response) {
//       console.log("Success");
//     },
//     error: function(request, status, error) {
//       console.log(status,error);
//     }
//   });
// };
