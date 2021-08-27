
// withdrawing a course
course = null
function changeAction(action){
  if(action.value=="Withdraw"){
    course=action.id
    $('#withdrawModal').modal('show');
    console.log($('#withdrawModal'));
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
