// withdrawing a course

function changeAction(action, course){

  if(action.value=="Withdraw"){
    withdraw(course) //This works now but there should be a "ARE YOU SURE YOU WANT TO DELETE EVERYING????" modal that pops up before this function is called.
  }
}

function withdraw(courseItem){
  // course =  courseItem.id.substring(11) // modeled this after trackVolunteers.js
  //                                       // how it's done in trackVolunteers.js is kinda dumb <--  the guy who wrote that code.
  course = courseItem
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
