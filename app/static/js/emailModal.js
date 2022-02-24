$(document).ready(function(){
  retrieveEmailTemplateData();
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

function showEmailModal(eventID, programID, selectedTerm) {
  $(".modal-body #eventID").val(eventID);
  $(".modal-body #programID").val(programID);
  $(".modal-body #selectedTerm").val(selectedTerm);

  for (let i=0; i < Object.keys(emailTemplateInfo).length; i++) {
    let option = `<option value='${emailTemplateInfo[i]['purpose']}'>${emailTemplateInfo[i]['subject']}</option>`;
    $('#templateIdentifier').append(option);
  }
  fetchEmailLogData().then(() => $('#emailModal').modal('show'));
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
        log = `Email was last sent to ${emailLog['recipients']} on ${emailLog['dateSent']}`
        $('#emailLastSent').text(log);
        $('#emailLastSent').attr('hidden', false);
      }
    }
  })
}

function replaceEmailBodyAndSubject() {
  let selected = $("#templateIdentifier option:selected" ).val();

  for (let i=0; i < Object.keys(emailTemplateInfo).length; i++) {
    if (emailTemplateInfo[i]['purpose'] == selected) {
      $('#subject').val(emailTemplateInfo[i]['subject']);
      $('#body').val(emailTemplateInfo[i]['body']);
    }
  }
}

$(function() {
  $('#emailModal').on('hidden.bs.modal', function () {
    $('#templateIdentifier option:not(:first)').remove();
  });
});
