// withdrawing a course

function changeAction(action){
  if(action.value=="Withdraw"){
    withdraw(action) //still working on this
  }
}

function withdraw(courseItem){
  course =  courseItem.id.substring(11) // modeled this after trackVolunteers.js
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
