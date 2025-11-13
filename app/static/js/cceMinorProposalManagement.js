$(document).ready(function() {
    $("#withdrawBtn").on("click", withdrawProposal);
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

function withdrawProposal(){
    // uses hidden label to withdraw course
    let proposalID = $("#proposalID").val();
    let username = $("#username").val()
    $.ajax({
        url: `/cceMinor/withdraw/${username}/${proposalID}`,
        type: "POST",
        success: function(s){
        window.location.href = `/profile/${username}/cceMinor?tab=manageProposals`
        },  
        error: function(request, status, error) {
            console.log(status, error);
        }
    })
    resetAllSelections()
};

window.changeAction = changeAction;
