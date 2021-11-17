
$(document).ready(function() {
  $('[data-bs-toggle="tooltip"]').tooltip();
// Search functionalities from the volunteer table in the UI
  $("#{{inputId}}").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#facultyTable").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  })
});
