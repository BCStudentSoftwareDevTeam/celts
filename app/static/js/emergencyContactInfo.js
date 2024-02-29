$(document).ready(function(){
    
    $('#emergencyContactEmail').on('input', function(){
        let emailAddress = $(this).val();
        if (emailAddress === '') {
            this.setCustomValidity('');
        } else if (!isValidEmailAddress(emailAddress)) {
            this.setCustomValidity('Please enter a valid email address.');
            this.reportValidity();
        } else {
            this.setCustomValidity('');
        }
    });

    function isValidEmailAddress(emailAddress) {
        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(emailAddress);
    }

    $('input.phone-input').inputmask('(999)-999-9999')
    $('input.phone-input').on('input', function(){
        let matches = $(this).val().match(/\d/g);
        let digits = matches?matches.length:0;
        if (digits == 0 || digits == 10){
            this.setCustomValidity('')
        }
        else{
            this.setCustomValidity('Please enter a valid phone number.')    
            this.reportValidity()        
        }
    })

    $('#saveExit').on('click', function(){
        let username = $('#username').attr('value')
        $('#contactForm').prop('action', `/profile/${username}/emergencyContact?action=exit`)
        if (formIsValid()){
            $('#contactForm').submit()
        }
    })

    $('#saveContinue').on('click', function(){
        let username = $('#username').attr('value')
        $('#contactForm').prop('action', `/profile/${username}/emergencyContact?action=continue`)
        if (formIsValid()){
            $('#contactForm').submit()
        }
    })
    
    function formIsValid(){
        let invalidInputs = $('input').map(function(i, e){
            if (!e.checkValidity()) {
                e.reportValidity();
                return e;
            }
        });
    
        return invalidInputs.length == 0;
    }
});