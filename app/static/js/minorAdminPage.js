import searchUser from './searchUser.js';

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
        console.table(responses);
        const cceBarChart = document.getElementById('cceChartByEngagement');

        const SEASONS = ["Spring", "Summer", "Fall"];
        function parseTerm(term) {
          const [season, year] = term.split(" ");
          return { season, year: Number(year) };
        }
        function termToIndex({ season, year }) {
          /**
           * converts a term like {season: "Fall", year: 2023} to an index for easier sorting
           * e.g., Spring 2023 -> 2023*3 + 0 = 6069
           *       Summer 2023 -> 2023*3 + 1 = 6070
           *       Fall 2023   -> 2023*3 + 2 = 6071
           */            
          return year * 3 + SEASONS.indexOf(season); 
        }
        function indexToTerm(idx) {
          /**
           * converts an index back to a term string
           * e.g., 6069 -> Spring 2023
           */
          const year = Math.floor(idx / 3);
          const season = SEASONS[idx % 3];
          return `${season} ${year}`;
        }

        const termMap = {};
        responses.forEach(r => {
          if (!termMap[r.termDescription]) {
            termMap[r.termDescription] = {
              engagement: 0,
              students: []
            };
          }
          termMap[r.termDescription].engagement += Number(r.engagementCount);
          termMap[r.termDescription].students.push(r.name);
        });

        const terms = Object.keys(termMap);
        const indices = terms.map(t => termToIndex(parseTerm(t)));
        const minIdx = Math.min(...indices);
        const maxIdx = Math.max(...indices);
        const labels = [];
        for (let i = minIdx; i <= maxIdx; i++) {
          labels.push(indexToTerm(i));
        }
        labels.forEach(t => {
          if (!termMap[t]) {
            termMap[t] = { engagement: 0, students: [] };
          }
        });

        const termEngagements = labels.map(t => termMap[t].engagement);
        const termStudents = labels.map(t => termMap[t].students);
        const maxEngagement = Math.max(...termEngagements) + 2;
        const cceLineChart = document.getElementById("cceChartByTerm");
        const completeByTerm = {};
        const incompleteByTerm = {};
        labels.forEach(t => {
          completeByTerm[t] = 0;
          incompleteByTerm[t] = 0;
        });

        responses.forEach(r => {
          if (r.completeSummer === "Yes") {
            completeByTerm[r.termDescription] += Number(r.engagementCount);
          } else {
            incompleteByTerm[r.termDescription] += Number(r.engagementCount);
          }
        });
        const completeEngagements = labels.map(t => completeByTerm[t] || 0);
        const incompleteEngagements = labels.map(t => incompleteByTerm[t] || 0);
        
        //Bar Chart
        if (barChart) barChart.destroy();
        barChart = new Chart(cceBarChart, {
          type: "bar",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Summer Incomplete",
                data: incompleteEngagements,
                backgroundColor: "red",
                stack: "summer"
              },
              {
                label: "Summer Complete",
                data: completeEngagements,
                backgroundColor: "green",
                stack: "summer"
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
              title: {
                display: true,
                text: "CCE Engagements by Term",
                font: { size: 18 }
              },
              legend: {
                display: true,
                position: "top"
              }
            },
            scales: {
              x: {
                stacked: true,
                title: { display: true, text: "Terms" }
              },
              y: {
                stacked: true,
                beginAtZero: true,
                max: maxEngagement,
                ticks: { stepSize: 1 },
                title: { display: true, text: "Engagement Count" }
              }
            }
          }
        });        
        if (lineChart) lineChart.destroy();
        //Line Chart
        lineChart = new Chart(cceLineChart, {
          type: "line",
          data: {
            labels: labels,
            datasets: [{
              label: "Engagement by Term",
              data: termEngagements,
              fill: false
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
              y: {
                beginAtZero: true,
                max: maxEngagement,
                ticks: { stepSize: 1 },
                title: {
                  display: true,
                  text: "Engagement Count"
                }
              },
              x: {
                title: {
                  display: true,
                  text: "Terms",
                }
              }
            },
            plugins: {
              title:{
                display: true,
                text: "CCE Engagements Trends over the Terms",
                font: {
                  size: 18
                }
              },
              tooltip: {
                callbacks: {
                  label: function (context) {
                    const idx = context.dataIndex;
                    return [
                      `Engagements: ${context.raw}`,
                      `Students: ${termStudents[idx].join(", ")}`
                    ];
                  }
                }
              }
            }
          }
        });
        function showBarChart() {
          $("#cceChartByEngagement").show();
          $("#cceChartByTerm").hide();
          setTimeout(() => barChart?.resize(), 0);
        }
        function showLineChart() {
          $("#cceChartByEngagement").hide();
          $("#cceChartByTerm").show();
          setTimeout(() => lineChart?.resize(), 0);
        }
        $("#chartButton").off("click").on("click", showBarChart);
        $("#lineButton").off("click").on("click", showLineChart);
      }
    });
  });
  $("#cceDownload").on("click", function(selected, fileName = "cceMinorChart.png"){
    const element = $(".ccePrint")[0]; 
    html2canvas(element).then(canvas => {
      console.log(canvas.getContext('2d'));
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

