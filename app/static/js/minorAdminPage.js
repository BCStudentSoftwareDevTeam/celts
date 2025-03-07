import searchUser from './searchUser.js'

function emailMinorCandidates(studentEmails){
  // If there are any students interested or declared, open the mailto link
  if (studentEmails.length) {
    const windowRef = window.open(`mailto:${studentEmails}`, '_blank');
    windowRef.focus();
    setTimeout(function(){
      if(!windowRef.document) {
          windowRef.close();
      }
    }, 500);
  } else {
    msgFlash("No interested or declared students to email.", "info")
  }
}

function emailAll(){
  let declaredStudentEmails =  $("#declaredStudentEmails").val();
  let interestedStudentEmails =  $("#interestedStudentEmails").val();
  let allMinorCandidateEmails = declaredStudentEmails + ";" + interestedStudentEmails;
  
  emailMinorCandidates(allMinorCandidateEmails);
}

$(document).ready(function() {
  $(document).on('click', '.remove_minor_candidate', function() {
      let username = $(this).attr('id'); 
      if ($('#declared').hasClass('show active')) {
        localStorage.setItem('activeTab', 'declared');
      }
      
      $.ajax({
          type: 'POST',
          url: '/profile/' + username + '/indicateInterest',
          success: function(response) {
            msgToast("Student successfully removed")
            location.reload();  
          },
          error: function(error) {
           console.log("error")
          }
      });
  });

$(document).on('click', '.declare_interested_student', function() {
  let username = $(this).attr('id');

  $.ajax({
      type: 'POST',
      url: '/profile/' + username + '/declareMinor',
      success: function(response) {
        msgToast("Student successfully declared")
        location.reload();
      },
      error: function(error) {
        console.log("error")
          } 
      });
  });

$(document).on('click', '.move_to_interested', function() {
  let username = $(this).attr('id');

  $.ajax({
      type: 'POST',
      url: '/profile/' + username + '/moveToInterested',
      success: function(response) {
        msgToast("Student successfully made interested")
        localStorage.setItem('activeTab', 'declared');
        location.reload();
      },
      error: function(error) {
        console.log("error")
          } 
      });
  });

$(document).ready(function() {
  setTimeout(function() {
  let activeTab = localStorage.getItem('activeTab');

  if (activeTab === 'declared') {
      $('#declared').addClass('show active'); 
      $('#interested').removeClass('show active'); 

      $('.nav-tabs .nav-link').removeClass('active'); 
      $('#declared-tab').addClass('active'); 

      localStorage.removeItem('activeTab'); 
      }
    }, 100);
  });
});

function getInterestedStudents() {
  // get all the checkboxes and return a list of users who's
  // checkboxes are selected
  let checkboxesDisplayedInModal = $("#addInterestedStudentsModal input[type=checkbox]:checked")
  let interestedStudentsList = []
  checkboxesDisplayedInModal.each(function(index, checkbox){
    interestedStudentsList.push(checkbox["value"])
  })
  return interestedStudentsList
}

function updateInterestedStudents(){
  let interestedStudentList = getInterestedStudents()
  let buttonContent = $("#addInterestedStudentsbtn").html()
  if (interestedStudentList.length > 1) {
    if (buttonContent.charAt(buttonContent.length-1) != "s") {
      // make the button text plural if there are multiple users selected
      $("#addInterestedStudentsbtn").html(buttonContent + "s")
    }
  } else if (buttonContent.charAt(buttonContent.length-1) == "s") {
    // remove the s if it is plural and we have less than 2 volunteers
    $("#addInterestedStudentsbtn").html(buttonContent.slice(0, -1))
  }
  // disable the submit button if there are no selectedCheckboxes
  if (interestedStudentList.length == 0) {
   
    $("#addInterestedStudentsbtn").prop("disabled", true)
  } else {
    $("#addInterestedStudentsbtn").prop("disabled", false)
  }
}

var userlist = []
function callback(selected) {
  let user = $("#addStudentInput").val()
  if (userlist.includes(selected["username"]) == false){
      userlist.push(user)
      let i = userlist.length;
      $("#interestedStudentList").prepend("<li class id= 'interestedStudentElement"+i+"'> </li>")          
      $("#interestedStudentElement"+i).append("<input  name = 'interestedStudents[]' type='checkbox' id= 'userlistCheckbox"+i+"' checked value='" + user +"' >  </input>",
       "<label form for= 'userlistCheckbox"+i+"'>"+ selected["firstName"]+ " " + selected["lastName"] +"</label>")
      $("#userlistCheckbox"+i).click(updateInterestedStudents)
      updateInterestedStudents()
  }
  else {
      msgFlash("User already selected.")
  }
}
$("#addInterestedStudentsbtn").prop('disabled', true);
+
$("#addInterestedStudentsModal").on("shown.bs.modal", function() {
  $('#addStudentInput').focus();
});

$("#addStudentInput").on("input", function() {
searchUser("addStudentInput", callback, true, "addInterestedStudentsModal");
});

$(document).ready(function() {
  $('#engagedStudentsTable').DataTable();
  $('#interestedStudentsTable').DataTable();
  $('#declaredStudentsTable').DataTable();

  $('#emailAllInterested').on('click', function() {
    emailMinorCandidates($("#interestedStudentEmails").val())
  });

  $('#emailAllDeclared').on('click', function() {
    emailMinorCandidates($("#declaredStudentEmails").val())
  });

  $('#emailAll').on('click', emailAll);
});

$(document).ready(function() {
  
})
