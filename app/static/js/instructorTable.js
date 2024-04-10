// Instructor manipulation functions
// -------------------------------------

export function getRowUsername(element) {
    return $(element).closest("tr").data("username")
}

export function createNewRow(selectedInstructor) {
  let instructor = (selectedInstructor["firstName"]+" "+selectedInstructor["lastName"]+" ("+selectedInstructor["email"]+")");
  let username = selectedInstructor["username"];
  let phone = selectedInstructor["phoneNumber"];
  let tableBody = $("#instructorTable").find("tbody");

  if(tableBody.prop('outerHTML').includes(instructor)){
    msgFlash("Instructor is already added.", "danger");
    return;
  }
  // Create new table row and update necessary attributes
  let lastRow = tableBody.find("tr:last");
  let newRow = lastRow.clone();

  let instructorName = newRow.find("td:eq(0) p")
  instructorName.text(instructor);

  let phoneInput = newRow.find("td:eq(0) input")
  phoneInput.val(phone);
  phoneInput.attr("id", "inputPhoneNumber-" +username);
  $(phoneInput).inputmask('(999)-999-9999');

  let removeButton = newRow.find("td:eq(1) button")
  let editLink = newRow.find("td:eq(0) a")
  editLink.attr("id", "editButton-" + username);

  editLink.attr("data-username", username)
  newRow.prop("hidden", false);
  lastRow.after(newRow);

  phoneInput.attr("data-value", phone)
  var edit = "#editButton-" + username
  var input = "#inputPhoneNumber-" + username
  if (username){
    setupPhoneNumber(edit, input)
  }

  $("#instructorTableNames").append('<input hidden name="instructor[]" value="' + username + '"/>')
}

export function getCourseInstructors() {
  // get usernames out of the table rows 
  return $("#instructorTableNames input").map((i,el) => $(el).val())
}