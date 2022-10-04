processPhoneSetup
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

function setupPhoneNumber(editButtonId, phoneInput, username){
  $(editButtonId).on('click', function() {
    var username = $(this).data("username")
    if ($(editButtonId).html() === 'Edit'){
      $(phoneInput).focus();
    }
    else{
      processPhoneSetup(this, phoneInput, username, "save")
    }
  });

  $(phoneInput).focus(function (){
    var username = $(editButtonId).data("username")
    processPhoneSetup(editButtonId, this, username, "edit")
  })
  $(phoneInput).focusout(function (event) {
    var username = $(editButtonId).data("username")
    var bla = $(editButtonId)
    if ($(event.relatedTarget).attr("id") != bla.attr("id")){
      processPhoneSetup(editButtonId, this, username, "restore")
    }
  })
}

function processPhoneSetup (editButtonId, phoneInputId, username, action) {
  if (action == "edit" ) {
    console.log("edit the phone")
    $(editButtonId).html("Save");
  }
  else if (action == "save" ) {
    console.log("save the phone")
    validatePhoneNumber(editButtonId, phoneInputId, username)
  }
  else if (action == "restore"){
    var phoneInput = $(phoneInputId);
    console.log("restore original phone number")
    $(phoneInputId).val(phoneInput.attr("data-value"))
    $(editButtonId).html('Edit');
  }
}

function validatePhoneNumber(editButtonId, phoneInputId, username) {

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
          msgToast("Phone Number", "Phone number successfully updated.")
      },
      error: function(request, status, error) {
          msgFlash("Phone number not updated.", "danger")
      }
    })
    $(editButtonId).html('Edit');
}

function reloadWithAccordion(accordionName) {
  var origin = window.location.href;

  if (origin.includes("?")){
    origin = origin.slice(0, origin.indexOf("?"));
  }

  location.replace(origin + "?accordion=" + accordionName);
}
