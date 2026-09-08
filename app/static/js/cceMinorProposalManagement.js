$(document).ready(function() {
    $("#withdrawBtn").on("click", function(){
        updateProposalStatus('withdraw')
    })
});

function changeAction(element) {
    const proposalId = element.id;
    const proposalType = $(element).data('type');
    const proposalAction = element.value;
    $('#proposalID').val(proposalId);

    if (proposalAction === "Edit") {
        location = `/cceMinor/edit${proposalType.replace(/\s+/g, '')}/${proposalId}`;
    } else if (proposalAction === "View") {
        location = `/cceMinor/view${proposalType.replace(/\s+/g, '')}/${proposalId}`;
    } else if (proposalAction === "withdraw") {
        $('#withdrawModal').modal('show');
    } else {
        updateProposalStatus(proposalAction.toLowerCase());
    }

    resetAllSelections();
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
