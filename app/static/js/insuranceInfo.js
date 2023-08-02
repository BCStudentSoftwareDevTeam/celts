$(document).ready(function(){

    $('#saveExit').on('click', function(){
        let username = $('#username').attr('value')
        $('#insuranceForm').prop('action', `/profile/${username}/insuranceInfo?action=exit`)
        if (formIsValid()){
            $('#insuranceForm').submit()
        }
    })

    $('#saveContinue').on('click', function(){
        let username = $('#username').attr('value')
        $('#insuranceForm').prop('action', `/profile/${username}/insuranceInfo?action=continue`)
        if (formIsValid()){
            $('#insuranceForm').submit()
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