$(document).ready(function(){

    $('#saveExit').on('click', function(){
        let username = $('#username').attr('value')
        $('#contactForm').prop('action', `/profile/${username}/emergencyContact?action=exit`)
        $('#contactForm').submit()
    })

    $('#saveContinue').on('click', function(){
        let username = $('#username').attr('value')
        $('#contactForm').prop('action', `/profile/${username}/emergencyContact?action=continue`)
        $('#contactForm').submit()
    })

    
});