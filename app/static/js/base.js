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
    $("select[name='newuser']").on('change', function(e) {
        $(e.target).parent().submit();
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

function setupPhoneNumber(editButtonId, phoneInput){
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
    $(editButtonId).html("Save");
  }
  else if (action == "save" ) {
    validatePhoneNumber(editButtonId, phoneInputId, username)
  }
  else if (action == "restore"){
    var phoneInput = $(phoneInputId);
    $(phoneInputId).val(phoneInput.attr("data-value"))
    $(editButtonId).html('Edit');
  }
}

function printDocument(path){
  // KNOWN ISSUE: Firefox and Chrome load pages differently, due to this we had to add a timeout that as a hack workaround 
  // but it still has some issues. 
  const printProposal = window.open(path);
  setTimeout(function () {
            printProposal.print();
            var timeoutInterval = setInterval(function() {
              printProposal.close();
              // No clearing the interval on purpose becuase firefox needs it to repeat.
            }, 30);
        }, 100);
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
        $(phoneInputId).attr("data-value",phoneInput.val())
        msgToast("Phone Number", "Successfully updated the phone number.")
      },
      error: function(request, status, error) {
        msgFlash("Phone number not updated.", "danger")
      },

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

function hasUniqueFileName(fileName){
  return $(".fileName[data-filename='" + fileName + "']").length == 0;
}

function getSelectedFiles(){
  let _fileHolder = new DataTransfer();
  $(".fileHolder").each(function(){
    _fileHolder.items.add($(this).data("file"));
  });
  return _fileHolder.files;
}

function handleFileSelection(fileInputId){
  var fileBoxId = "#" + fileInputId
  var attachedObjectContainerId = fileInputId + "Container"
  $(fileBoxId).after(`<div id="`+attachedObjectContainerId+`" class="py-0 px-0"></div>`)
  var objectContainerId = "#" + attachedObjectContainerId
  $(fileBoxId).on('change', function() {
    const selectedFiles = $(fileBoxId).prop('files');
    for (let i = 0; i < selectedFiles.length; i++){
      const file = selectedFiles[i];
      if (hasUniqueFileName(file.name)){
        let fileName = (file.name.length > 25) ? file.name.slice(0,10) + '...' + file.name.slice(-10) : file.name;
        let fileExtension = file.name.split(".").pop();
        let iconClass = '';
        switch(fileExtension) {
          case 'jpg': 
          case 'png':
          case 'jpeg':
            iconClass = "bi-file-image";
            break
          case 'pdf':
            iconClass = 'bi-filetype-pdf';
            break
          case 'docx':
            iconClass = 'bi-filetype-docx';
            break
          case 'xlsx':
            iconClass = 'bi-filetype-xlsx';
            break
          default:
            iconClass = 'bi-file-earmark-arrow-up';
        }
        let trashNum = ($(objectContainerId+ " .row").length)
        var fullTrashId = "#trash" + trashNum
        $(objectContainerId).append(" \
            <div class='border row p-0 m-0' id='attachedFilesRow" +trashNum+"'> \
              <i class='col-auto fs-3 px-3 bi " + iconClass + "'></i> \
              <div id='attachedFile" + trashNum + "' data-filename='" + file.name + "' class='fileName col-auto pt-2'>" + fileName + "</div> \
              <div class='col' style='text-align:right'> \
                <div class='btn btn-danger fileHolder p-1 my-1 mx-1' id='trash" + trashNum + "' data-filenum='" + trashNum + "'>\
                  <span class='bi bi-trash fs-6'></span>\
                </div>\
              </div> \
            </div>")
        $(fullTrashId).data("file", file);
        $(fullTrashId).data("file-container-id", attachedObjectContainerId);
        $(fullTrashId).on("click", function() {
          let elementFileNum = $(this).data('filenum');
          let attachedObjectContainerId = $(this).data('file-container-id');
          $("#"+ attachedObjectContainerId + " #attachedFilesRow" + elementFileNum).remove();
          $(fileBoxId).prop('files', getSelectedFiles());
        })
        $(fileBoxId).data("file-num", $(fileBoxId).data("file-num") + 1)
      }
      else{
        msgToast("File with filename '" + file.name + "' has already been added to this event")
      }
    }
    $(fileBoxId).prop('files', getSelectedFiles());
  });

}
