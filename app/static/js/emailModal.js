$(document).ready(function(){
  $("#body").on("blur", saveCursorIndex);
  $("#templateIdentifier").on("change", replaceEmailBodyAndSubject);
  $("#placeholderSelect").on("change", appendToBody);
  $("#cancel-btn").on("click", () => $('.modal').modal('hide'));
})

var emailTemplateInfo;
async function retrieveEmailTemplateData(eventId) {
   await $.ajax({
    url: `/retrieveEmailTemplate/${eventId}`,
    type: "GET",
    success: function(templateInfo) {
      emailTemplateInfo = templateInfo;
    },
    error: function(error, status){
        console.log(error, status);
    }
  });
}

var placeholderList;
async function retrievePlaceholderList(eventId){
  await $.ajax({
    url: `/retrievePlaceholderList/${eventId}`,
    type: "GET",
    success: function(placeholderInfo) {
      placeholderList = placeholderInfo;
    },
    error: function(error, status){
        console.log(error, status);
    }
  });
}

function readyTemplateOptions(eventId, template) {
  $('#templateIdentifier .template-option').remove()
  
  retrieveEmailTemplateData(eventId).then(function() {
    console.log(emailTemplateInfo)
    for (let i=0; i < Object.keys(emailTemplateInfo).length; i++) {
      let option = `<option class="template-option" value='${emailTemplateInfo[i]['purpose']}'>${emailTemplateInfo[i]['subject']}</option>`;
      $('#templateIdentifier').append(option);
    }
    if (template) $("#templateIdentifier").val(template);
    replaceEmailBodyAndSubject();
  })
}

function readyPlaceholderOptions(eventId) {
  $('#placeholderSelect .placeholder-option').remove()
  retrievePlaceholderList(eventId).then(function() {
    console.log(placeholderList)
    for (let i = 0; i < placeholderList.length; i++){
      let option = '<option class="placeholder-option" value="' + placeholderList[i][1] + '">'+ placeholderList[i][0] +'</option>';
      $('#placeholderSelect').append(option);
    }
  }); 
}



function showEmailModal(eventID, programID, selectedTerm, isPastEvent, template=null) {
  
  $(".modal-body #eventID").val(eventID);
  $(".modal-body #programID").val(programID);
  $(".modal-body #selectedTerm").val(selectedTerm);
  if (programID != "Unknown") {
    fetchProgramSender();  //adds another option for the from field if the event has a program
  } else{
    $("#emailSender option[value=optional]").hide();
  }
  if (isPastEvent) {
    $(".pastEventWarning").prop("hidden", false);
  } else {
    $(".pastEventWarning").prop("hidden", true);
  }



  $("#body").data("cursor-index", 0);
  readyTemplateOptions(eventID, template);

  readyPlaceholderOptions(eventID);
  fetchEmailLogData().then(() => $('#emailModal').modal('show'));
  
}

function saveCursorIndex(){
  $("#body").data("cursor-index", $("#body")[0].selectionStart);
}

function appendToBody() {  // Beans: change name to imply insertion
  bodyText = $("#body").val();
  cursorIndex = $("#body").data("cursor-index");
  console.log(cursorIndex);
  let metaData = $("#placeholderSelect option:selected" ).val();
  $("#body").val(bodyText.slice(0, cursorIndex) + metaData + bodyText.slice(cursorIndex));
  $("#body").data("cursor-index", cursorIndex + metaData.length);

  $("#placeholderSelect").val("")
}

async function fetchEmailLogData() {
  eventId = $(".modal-body #eventID").val();
  return await $.ajax({
    url: `/fetchEmailLogData/${eventId}`,
    type: 'GET',
    success: function(emailLog) {
      if (emailLog['exists'] == false) {
        $('#emailLastSent').attr('hidden', true);
      }
      else {
        $('#emailLastSent').text(emailLog['last_log']);
        $('#emailLastSentSubject').text(emailLog['last_log2']);
        $('#emailLastSent').attr('hidden', false);
      }
    }
  })
}

function fetchProgramSender() { // gets the sender name based on what is in the database
  var programInfo = {programId:$(".modal-body #programID").val()};
  $.ajax({

   url: "/getProgramSender/",
   type: "GET",
   data: programInfo,
   success: function(s) {
     var selectEmail = $("#senderEmail")
     selectEmail.html(s);
   },
   error: function(error, status){
       console.log(error, status);
   }
 });
}

function replaceEmailBodyAndSubject() {
  let selected = $("#templateIdentifier option:selected" ).val();

  for (let i=0; i < Object.keys(emailTemplateInfo).length; i++) {
    if (emailTemplateInfo[i]['purpose'] == selected) {
      $('#subject').val(emailTemplateInfo[i]['subject']);
      $('#body').val(emailTemplateInfo[i]['body']);
      $("#body").data("cursor-index", emailTemplateInfo[i]['body'].length)
    }
  }
}

$(function() {
  $('#emailModal').on('hidden.bs.modal', function () {
    $('#templateIdentifier option:not(:first)').remove();
  });
});
