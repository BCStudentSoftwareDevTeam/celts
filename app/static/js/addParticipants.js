$( document ).ready(function() {
    $(".Volunteers").hide();
    $(".outsidepart").hide();

});

function removeParticipants(btn) {

  var row = btn.parentNode.parentNode;
  row.parentNode.removeChild(row);
}

function removeVolunteer(btn) {

  var row = btn.parentNode.parentNode;
  row.parentNode.removeChild(row);

}

function searchParticipants() {
    let input = $('#Outsearch').val()
    input = input.toLowerCase();
    let x = $('.outsidepart');
    for (i = 0; i < x.length; i++) {
        if (!$('.outsidepart').index().html().toLowerCase().includes(input) || !input) {
            $(".outsidepart").hide();
        }
        else {
          $(".outsidepart").show();
        }
    }
}

function searchVolunteers() {
    let input = $('#Volsearch').val()
    input = input.toLowerCase();
    let x = $('.Volunteers');
    for (i = 0; i < x.length; i++) {
        if (!x[i].html().toLowerCase().includes(input) || !input) {
            $(".Volunteers").hide();
        }
        else {
            $(".Volunteers").show();
        }
    }
}

function textboxValue() {
firstName = $("#firstNameTextarea").value;
lastName = $("#lastNameTextarea").value;
emailEntry = $("#emailTextarea").value;
phoneNumber = $("#phoneNumberTextarea").value;
// $("#OutsideTable").append('<tr><td>{{ firstName + "" + lastName }}</td><td>{{ emailEntry }}</td> <td>{{ phoneNumber }}</td><td><button onclick="removeParticipants(this)" type="button">x</button></td></tr>');
}
