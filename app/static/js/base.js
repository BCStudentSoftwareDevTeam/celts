
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

function setupPhoneNumber(editButton, phoneInput){
  // input, button, username
  // setup all the event handlers
  // does not do any actions

  $(editButton).on('click', function() {
    var username = $(this).data("username")
    if ($(editButton).html() === 'Edit'){
      bloo(this, phoneInput, username, "edit")
    }
    else{
      bloo(this, phoneInput, username, "save")
    }
  });

  $(phoneInput).focus(function (){
    var username = $("#updatePhone").data("username")
    bloo("#updatePhone", this, username, "focus")
  })
  $(phoneInput).focusout(function () {
    var username = $("#updatePhone").data("username")
    bloo("#updatePhone", this, username, "focusout")
  })
}

function bloo (editButtonID, phoneInputID, username, action) {
  //second function that does all the actions that were setup in setupPhone
  // handler call
  if (action == "edit") {
    $(editButtonID).html("Save");
    $(phoneInputID).focus();
  }
  else if (action == "save" ) {
    validatePhoneNumber(editButtonID, phoneInputID, username)
  }
  else if (action == "focus") {
    $(editButtonID).html("Save");
  }
  // else if (action == "focusout"){
  //   $(editButtonID).html("Edit");
  // }
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
          msgFlash("Phone number is updated.", "success")
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
