$(document).ready(function() {

})
function changeAction(action){
    let proposalID = action.id;
    let proposalType = $(action).data('type')
    let proposalAction = action.value;
    // decides what to do based on selection
    if (proposalAction == "Edit"){
        location = `/cceMinor/edit${proposalType.replace(/\s+/g, '')}/` + proposalID;
    }
    if (proposalAction == "View"){
        location = `/cceMinor/view${proposalType.replace(/\s+/g, '')}/` + proposalID;
    }
    if (proposalAction == "Withdraw"){
        $('#proposalID').val(proposalID);
        $('#withdrawModal').modal('show');
       
      }
    resetAllSelections()
  }

function resetAllSelections() {
    $('.form-select').val('---');
}
window.changeAction = changeAction;