import searchUser from './searchUser.js'

$(document).ready(function() {
    $("#instructorTable").on("click", ".removeButton", function() {
        console.log("Please tell me")
        let closestRow =  $(this).closest("tr");
        let username = closestRow.data('username');
        console.log("If you can see me")

        $("#instructorTableNames input[value='" + username + "']").remove();
        console.log("I see you");
        closestRow.remove();
    });
    
    

    $("#courseInstructor").on('input', function() {
        searchUser("courseInstructor", createNewRow, true, null, "instructor");
        //sets autocomplete dropdown to top of screen stack
        setTimeout(function() {
            $(".ui-autocomplete").css("z-index", 9999);
        }, 500);
    });
    
    //for each row in instructorTable that has an instructor, pass that instructors phone data to setupPhoneNumber
    $('#instructorTable tr').each(function(){
        var username = getRowUsername(this)
        var edit = "#editButton-" + username
        var input = "#inputPhoneNumber-" + username
        if (username){
            setupPhoneNumber(edit, input)
        }
    });
});


function getRowUsername(element) {
    return $(element).closest("tr").data("username")
}

function createNewRow(selectedInstructor) {
    let instructor = (selectedInstructor["firstName"]+" "+selectedInstructor["lastName"]+" ("+selectedInstructor["email"]+")");
    let username = selectedInstructor["username"];
    let phone = selectedInstructor["phoneNumber"];
    let tableBody = $("#instructorTable").find("tbody");
  
    console.log("From new proposals selected instructors:", selectedInstructor, instructor, username, phone)
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
    console.log("Phone input is", phoneInput.val(phone))
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


