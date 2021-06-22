function removeParticipants() {

$("#row2").remove();
console.log("CLICK!")

}

function removeVolunteer() {

$("tr").filter(":contains(this)").remove()
console.log("CLICK!")

}
