$(document).ready(function(){
  $(".ban").click(function() {
    $("#banVolunteerButton").text($(this).val() + " Volunteer");
    $("#modalProgName").text("Program: " + $(this).closest("tr").children("td.programName").text());
    $('#banVolunteerModal').modal('toggle');
  });
















});
