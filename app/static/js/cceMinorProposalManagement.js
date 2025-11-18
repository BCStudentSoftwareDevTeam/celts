$(document).ready(function() {
    $("#withdrawBtn").on("click", function(){
        updateProposalStatus('withdraw')
    })
});
function changeAction(action){
    let proposalID = action.id;
    let proposalType = $(action).data('type')
    let proposalAction = action.value;
    // decides what to do based on selection
    if (proposalAction == "Edit"){
        location = `/cceMinor/edit${proposalType.replace(/\s+/g, '')}/` + proposalID;
    } else if (proposalAction == "View"){
        location = `/cceMinor/view${proposalType.replace(/\s+/g, '')}/` + proposalID;
    } else if (proposalAction == "Withdraw"){
        $('#proposalID').val(proposalID);
        $('#withdrawModal').modal('show');
    } else if (proposalAction == "Completed"){
        $('#proposalID').val(proposalID);
        updateProposalStatus('complete')
    }
    resetAllSelections()
  }

function resetAllSelections() {
    $('.form-select').val('---');
}

function updateProposalStatus(action){
    // for withdrawing proposals or marking them as complete
    let proposalID = $("#proposalID").val();
    let username = $("#username").val();

    $.ajax({
        url: `/cceMinor/${action}/${username}/${proposalID}`,
        type: "POST",
        success: function(res){
            window.location.href = `/profile/${username}/cceMinor?tab=manageProposals`;
        },
        error: function(request, status, error) {
            console.log(status, error);
        }
    });

    resetAllSelections();
}

window.changeAction = changeAction;
