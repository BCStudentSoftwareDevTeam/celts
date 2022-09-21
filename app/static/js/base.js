
function msgFlash(flash_message, status){
    if (status === "success") {
        category = "success";
        $("#flash_container").prepend('<div class=\"alert alert-'+ category + '\" role="alert" id="flasher">' + flash_message + '</div>');
        $("#flasher").delay(5000).fadeOut();
    }
    else {
        category = "danger";
        $("#flash_container").prepend("<div class=\"alert alert-"+ category +"\" role=\"alert\" id=\"flasher\">"+flash_message+"</div>");
        $("#flasher").delay(5000).fadeOut();
    }

}
$(document).ready(function() {
    $("#userSelect").on('change', function() {
        $("#userSelectForm").submit();
    });
    $(".alert").delay(5000).fadeOut();

});


function validatePhoneNumber(editButtonId, phoneInputId, username, whatsClicked) {
    if ($(editButtonId).html() === 'Edit' && ((whatsClicked == "button") || (whatsClicked == "input"))) {
        $(editButtonId).html("Save");
        $(phoneInputId).focus();
    } else if ($(editButtonId).html() === 'Save' && whatsClicked == "input") {
         //pass
    } else if ($(editButtonId).html() === 'Save' && (!$(phoneInputId).focus())){
        $(".inputPhone").css("border-color", "#fff");
    } else {
        // Save the phone number
        var phoneInput = $(phoneInputId);
        var isvalid = phoneInput.val().replace(/\D/g,"").length === 10;
        let isempty = phoneInput.val().replace(/\D/g,"").length === 0;       if (!(isvalid || isempty)) { // allows phone number input to be empty
            phoneInput.addClass("invalid");
            window.setTimeout(() => phoneInput.removeClass("invalid"), 1000);
            phoneInput.focus()
            return isvalid;
        }
          $.ajax({
            method:"POST",
            url:"/updatePhone",
            data:{"username":username,
                  "phoneNumber":phoneInput.val()},
            success: function(s){
                msgFlash("Phone number is updated.", "success")
            },
            error: function(request, status, error) {
                msgFlash("Phone number not updated.", "danger")
            }
          })
        $(editButtonId).html('Edit');
      }
}

function reloadWithAccordion(accordionName) {
  var origin = window.location.href;

  if (origin.includes("?")){
    origin = origin.slice(0, origin.indexOf("?"));
  }

  location.replace(origin + "?accordion=" + accordionName);
}
