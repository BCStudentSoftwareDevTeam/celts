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
        const $barChart = $("#cceChartByEngagement");
        const $lineChart = $("#cceChartByTerm");
        const barCanvas = document.getElementById("cceChartByEngagement");
        const lineCanvas = document.getElementById("cceChartByTerm");
        const SEASONS = ["Spring", "Summer", "Fall"];
        const termToIndex = (term) => {
          const [season, yearStr] = term.split(" ");
          return Number(yearStr) * 3 + SEASONS.indexOf(season);
        };
        const indexToTerm = (idx) => {
          const year = Math.floor(idx / 3);
          const season = SEASONS[idx % 3];
          return `${season} ${year}`;
        };
      
        // Build: term { engagement, students[], studentCounts{} }
        const byTerm = {};
      
        for (const r of responses) {
          const term = r.termDescription;
          const name = r.name;
          const count = Number(r.engagementCount) || 0;
      
          if (!byTerm[term]) {
            byTerm[term] = { engagement: 0, students: [], studentCounts: {} };
          }
      
          byTerm[term].engagement += count;
          byTerm[term].students.push(name);
          byTerm[term].studentCounts[name] = (byTerm[term].studentCounts[name] || 0) + count;
        }
        const existingTerms = Object.keys(byTerm);
      
        if (!existingTerms.length) {
          if (barChart) barChart.destroy();
          if (lineChart) lineChart.destroy();
          $barChart.hide();
          $lineChart.hide();
          return;
        }
        const indices = existingTerms.map(termToIndex);
        const minIdx = Math.min(...indices);
        const maxIdx = Math.max(...indices); 
        const labels = [];
        for (let i = minIdx; i <= maxIdx; i++) labels.push(indexToTerm(i));
      
        for (const term of labels) {
          if (!byTerm[term]) byTerm[term] = { engagement: 0, students: [], studentCounts: {} };
        }
        const termEngagements = labels.map((t) => byTerm[t].engagement);
        const maxEngagement = Math.max(...termEngagements) + 2;
      
        const isSummer = (term) => term.startsWith("Summer ");
        const barColorsByTerm = labels.map((t) => (isSummer(t) ? "blue" : "green"));
      
        const formatStudentCounts = (term) => {
          const counts = byTerm[term]?.studentCounts || {};
          const entries = Object.entries(counts);
          if (!entries.length) return "None";
          return entries.map(([name, cnt]) => `${name} (${cnt})`).join(", ");
        };
      
        const baseScales = {
          y: {
            beginAtZero: true,
            max: maxEngagement,
            ticks: { stepSize: 1 },
            title: { display: true, text: "Engagement Count" }
          },
          x: { title: { display: true, text: "Terms" } }
        };
      
        // Bar chart
        if (barChart) barChart.destroy();
      
        barChart = new Chart(barCanvas, {
          type: "bar",
          data: {
            labels,
            datasets: [
              {
                label: "Engagement by Term",
                data: termEngagements,
                backgroundColor: barColorsByTerm
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: baseScales,
            plugins: {
              title: {
                display: true,
                text: "CCE Engagements of Each Term",
                font: { size: 18 }
              },
              legend: {
                display: true,
                position: "top",
                labels: {
                  generateLabels: () => [
                    { text: "Summer Term", fillStyle: "blue", strokeStyle: "blue", lineWidth: 1 },
                    { text: "Non-Summer Term", fillStyle: "green", strokeStyle: "green", lineWidth: 1 }
                  ]
                }
              },
              tooltip: {
                callbacks: {
                  label: (context) => {
                    const term = labels[context.dataIndex];
                    return [
                      `Engagements: ${context.raw}`,
                      `Students: ${formatStudentCounts(term)}`
                    ];
                  }
                }
              }
            }
          }
        });
      
        // Line chart
        if (lineChart) lineChart.destroy();
      
        lineChart = new Chart(lineCanvas, {
          type: "line",
          data: {
            labels,
            datasets: [
              {
                label: "Engagement by Term",
                data: termEngagements,
                fill: false
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: baseScales,
            plugins: {
              title: {
                display: true,
                text: "CCE Engagements Trends over the Terms",
                font: { size: 18 }
              },
              tooltip: {
                callbacks: {
                  label: (context) => {
                    const term = labels[context.dataIndex];
                    return [
                      `Engagements: ${context.raw}`,
                      `Students: ${formatStudentCounts(term)}`
                    ];
                  }
                }
              }
            }
          }
        });

        // Toggle handlers
        const showBarChart = () => {
          $barChart.show();
          $lineChart.hide();
          setTimeout(() => barChart?.resize(), 0);
        };
        const showLineChart = () => {
          $barChart.hide();
          $lineChart.show();
          setTimeout(() => lineChart?.resize(), 0);
        };
      
        $("#chartButton").off("click").on("click", showBarChart);
        $("#lineButton").off("click").on("click", showLineChart);
        showBarChart();
      }      
    });
  });
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

