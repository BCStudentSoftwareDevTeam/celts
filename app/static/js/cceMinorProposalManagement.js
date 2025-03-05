$("#withdrawBtn").on("click", withdraw);

function changeAction(action){
    let proposalID = action.id;
    let proposalAction = action.value;
    // decides what to do based on selection
   if (proposalAction == "Withdraw"){
      $('#proposalID').val(proposalID);
      $('#withdrawModal').modal('show');
    }
  }


function withdraw(){
    // uses hidden label to withdraw course
    let proposalID = $("#proposalID").val();
    $.ajax({
      url: `/cceMinor/withdraw/${proposalID}`,
      type: "POST",
      success: function(s){
        location.reload()
      },
      error: function(request, status, error) {
          console.log(status,error);
      }
    })
  };


window.changeAction = changeAction;
