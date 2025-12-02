import searchUser from './searchUser.js'

$(document).ready(function() {
  // Load flash message from sessionStorage, if any
  msgFlash();

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
            msgFlash("Candidate minor successfully removed", "success", 1500, true);
            location.reload();
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
  let barChart = null;
  let lineChart = null;
  $("#cceMinor").on("click", function(){
    let username = $(this).data("username");
    $.ajax({
      type: 'GET',
      url: '/profile/' + username + '/cceMinorChart',
      success: function (responses) {
          const names = [];
          const engagements = [];
          const barColors = [];
          responses.forEach(r => {
              names.push(r.name);
              engagements.push(r.engagementCount);
              barColors.push(r.completeSummer === "Yes" ? "green" : "red");
          });
          const maxValue = Math.max(...engagements) + 2;
          const cceBarChart = document.getElementById('cceChartByEngagement');
          if (barChart) barChart.destroy();
          barChart = new Chart(cceBarChart, {
              type: "bar",
              data: {
                  labels: names,
                  datasets: [{
                      backgroundColor: barColors,
                      data: engagements
                  }]
              },
              options: {
                  plugins: {
                      legend: { display: false }
                  },
                  scales: {
                      y: {
                          beginAtZero: true,
                          max: maxValue,
                          ticks: { stepSize: 1 }
                      }
                  }
              }
          });
          const termMap = {};
          responses.forEach(r => {
              if (!termMap[r.termDescription]) {
                  termMap[r.termDescription] = {
                      engagement: 0,
                      students: []
                  };
              }
              console.log(r.engagementCount);
              termMap[r.termDescription].engagement += Number(r.engagementCount);
              console.table(termMap);
              termMap[r.termDescription].students.push(r.name);
          });
          const sortedTerms = Object.keys(termMap).sort();
          const termEngagements = sortedTerms.map(t => termMap[t].engagement);
          const termStudents = sortedTerms.map(t => termMap[t].students);
          const maxEngagement = Math.max(...termEngagements) + 2;
          const cceLineChart = document.getElementById("cceChartByTerm");
          if (lineChart) lineChart.destroy();
          lineChart = new Chart(cceLineChart, {
              type: "line",
              data: {
                  labels: sortedTerms,
                  datasets: [{
                      label: "Engagement by Term",
                      borderColor: "blue",
                      fill: false,
                      data: termEngagements
                  }]
              },
              options: {
                  responsive: true,
                  scales:{
                      y: {
                          beginAtZero: true,
                          max: maxEngagement,
                          ticks: { stepSize: 1 },
                          title:{
                          display: true,
                          text: 'Engagement Count'
                          }
                      },
                      x: {
                        title:{
                        display: true,
                        text: 'Terms'
                        }
                      },
                  },
                  plugins: {
                      tooltip: {
                          callbacks: {
                              label: function (context) {
                                  console.table(context);
                                  const idx = context.dataIndex;
                                  const value = context.raw;
                                  const students = termStudents[idx].join(", ");
                                  return [
                                      `Engagements: ${value}`,
                                      `Students: ${students}`
                                  ];
                              }
                          }
                      }
                  }
              }
          });

          $("#chartButton").off().on("click", function () {
              $("#cceChartByEngagement").show();
              $("#cceChartByTerm").hide();
          });
          $("#dataButton").off().on("click", function () {
              $("#cceChartByEngagement").hide();
              $("#cceChartByTerm").show();
          });
      }
  });
  });

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
    msgFlash("Succssesfully added student intrested in minor.", "success", 1300, true)
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

