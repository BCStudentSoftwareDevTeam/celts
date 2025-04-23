import searchUser from './searchUser.js'

$(document).ready(function() {
  $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
    let activeTab = $(e.target).attr('id').replace('-tab', '');
    let newUrl = window.location.pathname + '?tab=' + activeTab;
    history.pushState(null, '', newUrl);
  });

  $('.remove_minor_candidate').on('click', function() {
      let username = $(this).attr('id'); 
      let isAdding = false
      
      $.ajax({
          type: 'POST',
          url: '/profile/' + username + '/indicateInterest',
          data: JSON.stringify({ "isAdding": isAdding }),
          contentType: "application/json",
          success: function(response) {
            location.reload()
          },
          error: function(error) {
           console.log("error")
          }
      });
  });


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

  $(".updateMinorInterestButton").on("click", function(e){
    e.preventDefault();
    let interestForm = $("#updateMinorInterestForm");
    let url = $(this).data("url");
    let activeTab = $(".nav-tabs .active").attr("id").replace("-tab", "");

    // Append the active tab to the form action URL
    interestForm.attr("action", url + "?tab=" + activeTab);
    interestForm.submit();
    });

  let urlParams = new URLSearchParams(window.location.search);
  let activeTab = urlParams.get('tab');
  if (activeTab) {
      $('#studentTabs button[data-bs-target="#' + activeTab + '"]').tab('show');
  }
  $("#cceMinor").on("click", function(){
    let username = $(this).data("username");
    const xValues = [];
    const yValues = [];
    const barColors = [];

    $.ajax({
      type: 'GET',
      url: '/profile/' + username + '/cceMinorChart',
      data: JSON,
      success: function(responses) {
        for (let i = 0; i < responses.length; i++){
          xValues.push(responses[i].engagementCount);
          yValues.push(responses[i].name);
          barColors.push(responses[i].completeSummer === "Yes" ? "green" : "red");
        }
        const cceChart = document.getElementById('cceChartGen');
        const maxValue = Math.max(...xValues.map(Number))+2;

        if (cceChart) {
          new Chart(cceChart, {
            type: "bar",
            data: {
              labels: yValues,
              datasets: [{
                label: "Summer Completed",
                backgroundColor: barColors,
                data: xValues
              }]
            },
            options: {
              scales:{
                y: {
                  beginAtZero: true,
                  max: maxValue,
                  title:{
                    display:true,
                    text:'Hours of Engagements',
                    font: {
                      family: 'Inter',
                      size: 16,
                      weight: 'bold'
                    }
                  }
                },
                x: {
                  title:{
                    display:true,
                  }
                }
              },
              plugins: {
                legend: {
                  display: false,
                },
                tooltip: {
                  callbacks: {
                    label: function(context) { 
                      const value = context.formattedValue;
                      const completed = barColors[context.dataIndex] === "green" ? "Yes" : "No";
                      return [
                        `Engagements: ${value}`,
                        `Summer Completed: ${completed}`
                       ];
                    }
                  }
                }
              }
            }
          });
        }
      },
      error: function(error) {
        console.log("error: " + error);
      }
    });
  })

  // Download the chart as an image
  $("#cceDownload").on("click", function(selected, fileName = "cceMinorChart.png"){
    const element = $(".ccePrint")[0]; 

    html2canvas(element).then(canvas => {
      const downloadLink = document.createElement('a');
      downloadLink.href = canvas.toDataURL(); 
      downloadLink.download = fileName; 
      downloadLink.click();
    })
  })
})


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
    msgFlash("No candidates to email.", "info")
  }
}

function emailAll(){
  let declaredStudentEmails =  $("#declaredStudentEmails").val();
  let interestedStudentEmails =  $("#interestedStudentEmails").val();
  let allMinorCandidateEmails = declaredStudentEmails + ";" + interestedStudentEmails;
  
  emailMinorCandidates(allMinorCandidateEmails);
}

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

