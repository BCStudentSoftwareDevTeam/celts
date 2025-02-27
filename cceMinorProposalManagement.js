$("#withdrawBtn").on("click", withdraw);



function changeAction(action){
    let courseID = action.id;
    let courseAction = action.value;
    // decides what to do based on selection
    if (courseAction == "Renew"){
      $('#courseID').val(courseID);
      updateRenewModal(courseID)
      $("#renewModal").modal('show')
    } else if (courseAction == "View"){
      location = '/serviceLearning/viewProposal/' + courseID;
    } else if (courseAction == "Withdraw"){
      $('#courseID').val(courseID);
      $('#withdrawModal').modal('show');

    }
}