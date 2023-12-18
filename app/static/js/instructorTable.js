function createNewRow(selectedInstructor) {
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

function getRowUsername(element) {
    return $(element).closest("tr").data("username")
}

function getCourseInstructors() {
    // get usernames out of the table rows into an array
    return $("#instructorTableNames input").map((i,el) => $(el).val())
}

// Add course instructor event handlers
// -----------------------------------------
$("#instructorTable").on("click", "#remove", function() {
    let closestRow =  $(this).closest("tr")
    $("#instructorTableNames input[value="+closestRow.data('username')+"]").remove()
    closestRow.remove();
    });
    $("#courseInstructor").on('input', function() {
        searchUser("courseInstructor", createNewRow, true, null, "instructor");
    });

    // for each row in instructorTable that has an instructor, pass that instructors phone data to setupPhoneNumber
    $('#instructorTable tr').each(function(){
    var username = getRowUsername(this)
    var edit = "#editButton-" + username
    var input = "#inputPhoneNumber-" + username
    if (username){
        setupPhoneNumber(edit, input)
    }
})
