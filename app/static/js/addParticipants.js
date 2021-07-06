// $(document).ready(function(){
//   $(".Volunteers").hide();
//   $("#Volsearch").on("keyup", function() {
//     var value = $(this).val().toLowerCase();
//     $("#Volul a").filter(function() {
//       $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
//       if(!value) {
//         $(".Volunteers").hide();
//       }
//     });
//   });
// });

function searchVolunteer(){
  $("#volunteerInput").autocomplete({
    source: "../../controllers/admin/addParticipants.py",
    minLength: 2,
  });
};


function addVolunteer(e){
  volunteersName = $(e).text()
  $("#Volunteertable").append('<tr><td>' + volunteersName + '</td><td><button id="removeButton" onclick="removeVolunteer(this)" type="button">x</button></td></tr>')
  console.log(volunteersName)

}
function removeParticipant(e) {
  text = $(e).parent().parent()[0].textContent;
  console.log(text)
  $(e).parent().parent().remove();
}

function removeVolunteer(e) {
  $(e).parent().parent().remove();
}

count = 0;
function addOutsideParticipant() {
  firstName = $("#firstNameTextarea").val();
  lastName = $("#lastNameTextarea").val();
  emailEntry = $("#emailTextarea").val();
  phoneNumber = $("#phoneNumberTextarea").val();
  $("#OutsideTable").append('<tr id="removeRow"><td>' + firstName + " " + lastName + " " + '</td><td>' + emailEntry + " " +'</td><td>' + phoneNumber + " " + '</td><td><button id="removeButton" onclick="removeParticipant($(this))" type="button">x</button></td></tr>');
  opList = ["email", "firstName", "lastName", "phoneNumber"];
  opList.forEach(item => {
    $("<input type='text'hidden />")
    .attr("value", $('#'+item+'Textarea').val())
    .attr("id", item+count)
    .attr("name", item+count)
    .appendTo("#OutsideTable")
    $('#'+item+'Textarea').val('').blur();
  })
  // tempList = [];
  // $(this)
  // .attr("class", count)
  // tempList.push($(this));
  // console.log($(this).getAttribute("class"));
  // console.log(tempList[0][0].emailEntry);
  count++;
  $('#particpantsModal').modal('hide')
}
