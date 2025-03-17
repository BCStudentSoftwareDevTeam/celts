$(document).ready(function() {
    console.log("hola")

})
function changeAction(action){
    console.log(action)
    let proposalID = action.id;
    let proposalType = $(action).data('type')
    let proposalAction = action.value;
    // decides what to do based on selection
    if (proposalAction == "Edit"){
        location = `/cceMinor/edit${proposalType.replace(/\s+/g, '')}/` + proposalID;
    }
  }
window.changeAction = changeAction;