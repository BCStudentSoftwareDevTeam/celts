// This file only contains the javascript settings for reports.html. 
// To see the data configuration settings, go to app/static/js/reports_data.js

// constants 
const modal = $('#viz-modal');
const openModalBtn = $('#open-viz-modal');
const closeModalBtn = $('#close-viz-modal');

function initializeCharts() {
  // Bar chart for Total Hours By Program
  const chartData1 = {
    type: 'bar',
    data: {
      labels: ['Computer Science', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: '# of Hours',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  };
  new Chart($('#chart1'), chartData1);

  // Pie chart for Hours By Major
  const pieData = {
    type: 'pie',
    data: {
      labels: ['Computer Science', 'Engineering', 'Mathematics', 'Physics', 'Chemistry'],
      datasets: [{
        label: 'Hours By Major',
        data: [20, 15, 25, 30, 10],
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Hours By Major'
        }
      }
    }
  };
  new Chart($('#chart2'), pieData);
}

$(document).ready(function() { 
  initializeCharts();
  openModal();
  closeModal();


  
});

function openModal() {
  openModalBtn.on("click", function() {
  modal.css("display", "block");
  })
}

function closeModal() {
  closeModalBtn.on("click", function() {
    modal.css("display", "none");
  })
}





