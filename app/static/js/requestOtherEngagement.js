$(document).ready(function(){

    $('#saveExit').on('click', function(){
        let username = $('#username').attr('value')
        $('#requestOtherCommEng').prop('action', `/profile/${username}/requestOtherCommEng?action=exit`)
        if (formIsValid()){
            $('#requestOtherCommEng').submit()
        }
    })

    $('#saveContinue').on('click', function(){
        let username = $('#username').attr('value')
        $('#requestOtherCommEng').prop('action', `/profile/${username}/requestOtherCommEng?action=continue`)
        if (formIsValid()){
            $('#requestOtherCommEng').submit()
        }
    })

    function formIsValid(){
        let invalidInputs = $('input').map(function(i, e){
            if (! e.checkValidity()) {
                e.reportValidity()
                return e
            }
        })
        return invalidInputs.length == 0
    }
});
