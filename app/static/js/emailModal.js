var emailTemplateInfo;

function showEmailModal(eventID, programID, selectedTerm) {
  $(".modal-body #eventID").val(eventID);
  $(".modal-body #programID").val(programID);
  $(".modal-body #selectedTerm").val(selectedTerm);

   $.ajax({
    url: "/renderEmailModal",
    type: "GET",
    success: function(templateInfo) {
      emailTemplateInfo = templateInfo;
      for (let i=0; i < Object.keys(templateInfo).length; i++) {
        let option = `<option value='${templateInfo[i]['purpose']}'>${templateInfo[i]['subject']}</option>`;
        $('#templateIdentifier').append(option);
      }
      $('#emailModal').modal('show');
    },
    error: function(error, status){
        console.log(error, status);
    }
  });
}

function replaceBody() {
  let selected = $("#templateIdentifier option:selected" ).val();

  for (let i=0; i < Object.keys(emailTemplateInfo).length; i++) {
    if (emailTemplateInfo[i]['purpose'] == selected) {
      $('#subject').val(emailTemplateInfo[i]['subject']);
      $('#body').val(emailTemplateInfo[i]['body'])
    }
  }
}
