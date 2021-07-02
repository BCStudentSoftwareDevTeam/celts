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

function volunteerSearch() {
  $("#volunteerInput").autocomplete({
      source: '/addParticipants',
      minLength: 2,
      select: function( event, ui ) {
        log( "Selected: " + ui.item.value + " aka " + ui.item.id );
      }
    })
  }


function addVolunteer(e){
  volunteersName = $(e).text()
  $("#Volunteertable").append('<tr><td>' + volunteersName + '</td><td><button id="removeButton" onclick="removeVolunteer(this)" type="button">x</button></td></tr>')
  console.log(volunteersName)

}
function removeParticipants(e) {
  text = $(e).parent().parent()[0].textContent;
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
  $("#OutsideTable").append('<tr id="removeRow"><td>' + firstName + " " + lastName + " " + '</td><td>' + emailEntry + " " +'</td><td>' + phoneNumber + " " + '</td><td><button id="removeButton" onclick="removeParticipants(this)" type="button">x</button></td></tr>');

  opList = ["email", "firstName", "lastName", "phoneNumber"];
  opList.forEach(item => {
    $("<input type='text' hidden/>")
    .attr("value", $('#'+item+'Textarea').val())
    .attr("id", item+count)
    .attr("name", item+count)
    .appendTo("#OutsideTable")
    $('#'+item+'Textarea').val('').blur();
  })
  count++;
  $('#particpantsModal').modal('hide')
}
