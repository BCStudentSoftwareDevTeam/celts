$("#withdrawBtn").on("click", withdraw);

function changeAction(action){
    let proposaltype = action.id;
    let proposalAction = action.value;
    // decides what to do based on selection
   if (proposalAction == "Withdraw"){
      $('#proposaltype').val(proposaltype);
      $('#withdrawModal').modal('show');
    }
  }


function withdraw(){
    // uses hidden label to withdraw course
    let proposalType = $("#proposaltype").val();
    $.ajax({
      url: `/cceMinor/withdraw/${proposalType}`,
      type: "POST",
      success: function(s){
        location.reload();
      },
      error: function(request, status, error) {
          console.log(status,error);
      }
    })
  };


window.changeAction = changeAction;
