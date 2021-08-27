
// withdrawing a course
course = null
function changeAction(action){
  if (action.value=="Renew"){
    // Renew

  } else if (action.value=="View"){
    // View

  } else if (action.value=="Withdraw"){
    course=action.id
    $('#withdrawModal').modal('show');

  } else if(action.value=="Edit"){
    // Edit
  }
}

function withdraw(){
  $.ajax({
    url: "/withdrawCourse/"+ course,
    type: "POST",
    success: function(s){
      location.reload()
    },
    error: function(request, status, error) {
        console.log(status,error);
      }
  })
}
