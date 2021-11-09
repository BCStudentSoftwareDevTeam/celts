function changeTerm() {

    $('form').submit();
};

function formSubmit(el) {
  $("#termSelector").attr('action', '/courseManagement/' + el);
  $("#termSelector").submit()
}
