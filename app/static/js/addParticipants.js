function removeParticipants(btn) {

  var row = btn.parentNode.parentNode;
  row.parentNode.removeChild(row);
}

function removeVolunteer(btn) {

var row = btn.parentNode.parentNode;
row.parentNode.removeChild(row);

}


function searchParticipants() {
    let input = document.getElementById('Outsearch').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('outsidepart');

    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="list-item";
        }
    }
}

function searchVolunteers() {
    let input = document.getElementById('Volsearch').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('Volunteers');

    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="list-item";
        }
    }
}
