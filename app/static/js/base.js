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
});

function validatePhoneNumber(editButtonId, phoneInputId, username) {
    var isvalid = null
    if ($(editButtonId).html() === 'Edit') {
        $(editButtonId).html("Save");
        $(phoneInputId).focus();
    } else {
        // Save the phone number
        var phoneInput = $(phoneInputId);
        isvalid = phoneInput.val().replace(/\D/g,"").length === 10;
        let isempty = phoneInput.val().replace(/\D/g,"").length === 0;
        if (!(isvalid || isempty)) {
            phoneInput.addClass("invalid");
            window.setTimeout(() => phoneInput.removeClass("invalid"), 1000);
            phoneInput.focus()
            isvalid = false;
            return isvalid;
        }
        if (isvalid == true){
          $.ajax({
            method:"POST",
            url:"/updatePhone",
            data:{"username":username,
                  "phoneNumber":phoneInput.val()},
            success: function(s){
              msgFlash("Phone Number is updated", "success")
            },
            error: function(request, status, error) {
              msgFlash("Error updating phone number", "danger")
            }
          })
      } else if (isvalid == false){
          msgFlash("Invalid Phone number", "danger")
        }

        $('#phoneInput').inputmask('(999)-999-9999');
        $(editButtonId).html('Edit');
    }


}
