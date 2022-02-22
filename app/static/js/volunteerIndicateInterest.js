$(document).ready(function() {
  $(".form-check-input").click(function updateInterest(el){
    var programID = $(this).attr('id');
    var interest = $(this).is(':checked');
    if (interest) {
      var routeUrl = "/addInterest/"
    }
    else {
      var routeUrl = "/deleteInterest/"
    }
    $.ajax({
      method: "POST",
      url: routeUrl + programID,
      success: function(response) {
          msgFlash("Your interest has been updated", "success")
      },
      error: function(request, status, error) {
        console.log(status,error);
        msgFlash("Error Updating Interest", "danger")
        window.location.reload(true);
      }
    });
  });
});


function updateManagers(el,user,status){
  var programID = el.id;
  var user = (user[0].id);
  if (status == undefined){
    status = true;
  }
  let data = {
      programID : programID,
      user : user,
      status:status,
      from: "ajax"
  }
  $.ajax({
    url: "/updateManagers",
    type: "POST",
    data: data,
    success: function(s){
        location.reload()
      },
      error: function(error, status){
          console.log(error, status)
        }
    })
  }

function updateBackgroundCheck(user,bgType){
  let checkPassed = $( "#"+bgType).val();
  let data = {
      checkPassed : checkPassed,
      user: user.id,
      bgType: bgType
  }
  $.ajax({
    url: "/updateBackgroundCheck",
    type: "POST",
    data: data,
    success: function(s){
      location.reload()
    },
    error: function(error, status){
        console.log(error, status)
      }
    })
  }
