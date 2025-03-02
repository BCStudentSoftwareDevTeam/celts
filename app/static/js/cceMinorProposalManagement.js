function changeAction(action){
    let proposalID = action.id;
    let proposalAction = action.value;


    console.log(proposalAction);
    console.log(proposalID)
    // decides what to do based on selection
   if (proposalAction == "Withdraw"){
      $('#proposalID').val(proposalID);
      $('#withdrawModal').modal('show');

    }
  }


window.changeAction = changeAction;
