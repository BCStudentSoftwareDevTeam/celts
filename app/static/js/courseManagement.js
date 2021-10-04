function changeTerm() {

    $('form').submit();
};

function formSubmit(el){
  $("#termSelector").attr('action', '/' + el + '/courseManagement');
  $("#termSelector").submit()
}
