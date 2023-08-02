$(document).ready(function(){

    $('#saveExit').on('click', function(){
        let username = $('#username').attr('value')
        $('#insuranceForm').prop('action', `/profile/${username}/insuranceInfo?action=exit`)
        $('#insuranceForm').submit()
    })

    $('#saveContinue').on('click', function(){
        let username = $('#username').attr('value')
        $('#insuranceForm').prop('action', `/profile/${username}/insuranceInfo?action=continue`)
        $('#insuranceForm').submit()
    })

    
});