$(document).ready(function(){
  retrieveEmailTemplateData();

  $("#beans").on("click", appendToBody)

})
var emailTemplateInfo;
function retrieveEmailTemplateData() {
   $.ajax({
    url: "/retrieveEmailTemplate",
    type: "GET",
    success: function(templateInfo) {
      emailTemplateInfo = templateInfo;
    },
    error: function(error, status){
        console.log(error, status);
    }
  });
}

// var placeholderData;
// function retrievePlaceholderData(eventId){
//   $.ajax({
//     url: `/retrievePlaceholderData/${eventId}`,
//     type: "GET",
//     success: function(placeholderInfo) {
//       placeholderData = placeholderInfo;
//     },
//     error: function(error, status){
//         console.log(error, status);
//     }
//   });
// }

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

  for (let i=0; i < Object.keys(emailTemplateInfo).length; i++) {
    let option = `<option value='${emailTemplateInfo[i]['purpose']}'>${emailTemplateInfo[i]['subject']}</option>`;
    $('#templateIdentifier').append(option);
  }
  if (template) $("#templateIdentifier").val(template);
  // for (let i=0; i < Object.keys(emailTemplateInfo).length; i++) {
  //   let option = `<option value='${emailTemplateInfo[i]['purpose']}'>${emailTemplateInfo[i]['subject']}</option>`;
  // }

  $("#body").data("cursor-index", 0);
  replaceEmailBodyAndSubject();
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
