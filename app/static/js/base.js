
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

    toastElementList = [].slice.call(document.querySelectorAll('.toast'))
    toastList = toastElementList.map(function (toastEl) {
       return new bootstrap.Toast(toastEl)
   })

});

function msgToast(head, body){
  if ($("#liveToast").is(":visible") == true){
    $('#liveToast').removeClass("show")
    $('#liveToast').addClass("hide")
  }
  $("#toast-header").html(head)
  $("#toast-body").html(body)
  toastList[0].show()
}

function validatePhoneNumber(editButtonId, phoneInputId, username) {
    if ($(editButtonId).html() === 'Edit') {
        $(editButtonId).html("Save");
        $(phoneInputId).focus();
    } else {
        // Save the phone number
        var phoneInput = $(phoneInputId);
        var isvalid = phoneInput.val().replace(/\D/g,"").length === 10;
        let isempty = phoneInput.val().replace(/\D/g,"").length === 0;
        if (!(isvalid || isempty)) { // allows phone number input to be empty
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

//set character limit and calculate remaining characters
function setCharacterLimit(textboxId, labelId){
  var maxCharacters = 1800;
  var textLength = 0;
  var textValue = $(textboxId).val();
  var textLength = textValue.length;
  $(labelId).text("Remaining Characters: " + (maxCharacters - textLength));
  if (textLength > maxCharacters){
      $(textboxId).val(textValue.substring(0, maxCharacters));
      $(labelId).text("Remaining Characters: " + 0);
  }
}
