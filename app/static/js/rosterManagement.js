import searchUser from './searchUser.js'

$(document).ready(function(){
    var dt = $('#rosterTable').DataTable();

    searchUser("searchStudentsInput", callback, "searchStudentsInput");   // initialize ONCE

  $("#searchIcon").click(function (e) {
    e.preventDefault();
    callback($("#searchStudentsInput").val());
  });

  $("#searchStudentsInput").focus();

  $("#dismissModal").click(function() {
    location.reload();
  })
});

function callback(selected) {
  var form = $("#searchStudentForm");
  form.attr("action", "/" + selected["username"] + "/addInterest/" + form.data("program") + "/False");    
  $("#searchStudentForm").submit();  
}

$('#searchStudentForm').on('submit', function(e) {
    e.preventDefault(); // stops the browser's normal form submission/redirect

  var formData = $(this).serialize(); // or new FormData(this) if you have file inputs
  $.ajax({
    url: $(this).attr('action'),
    type: $(this).attr('method') || 'POST',
    success: function(response) {
        var targetDiv = $("#addedNameDivTarget");
        var targetP = $("#addedNameToClone").clone();
        targetDiv.append(targetP);
        var targetSpan = targetP.find(".addedNameTarget");
        targetSpan.text(response['firstName'] + " " + response["lastName"]);
        targetP.attr("hidden", false);
    },
    error: function(xhr, status, error) {
        var targetDiv = $("#addedNameDivTarget");
        var targetP = $("#addedNameToClone");
        var targetSpan = targetP.find(".addedNameTarget");
        targetP.html(targetSpan);
        targetSpan.text("Uh oh... something went wrong. Contact a CELTS staff member.");
        targetP.attr("hidden", false);
        console.log(status, error);
    }
  })
});

$("#exportRoster").click(function() {
  var year = $(this).data("year");
  var program = $(this).data('program');
  $.ajax({
    url: "/exportRosters/" + program + "/" + year,
    type: 'GET',
    success: function(response) {
        console.log(response)
    },
    error: function(xhr, status, error) {      
        console.log(status, error);
    }
  })
})