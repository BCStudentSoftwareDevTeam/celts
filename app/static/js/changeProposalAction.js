// withdrawing a course

function changeAction(action){

  if(action.value=="Withdraw"){
    withdraw(action.id) //This works now but there should be a "ARE YOU SURE YOU WANT TO DELETE EVERYING????" modal that pops up before this function is called.
  }
}

function withdraw(course){
  // course =  courseItem.id.substring(11) // modeled this after trackVolunteers.js
  //                                       // how it's done in trackVolunteers.js is kinda dumb <--  the guy who wrote that code.
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
