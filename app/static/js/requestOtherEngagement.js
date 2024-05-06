import { validateEmail } from "./emailValidation.mjs";

$(document).ready(function(e) {

    $("input.phone-input").inputmask('(999)-999-9999');
    $("input.email-input").on('input', validateEmail)


});


