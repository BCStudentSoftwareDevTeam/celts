function isValidEmailAddress(emailAddress) {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(emailAddress);
}

export function validateEmail(){
    let emailAddress = $(this).val();
    if (emailAddress === '') {
        this.setCustomValidity('');
    } else if (!isValidEmailAddress(emailAddress)) {
        this.setCustomValidity('Please enter a valid email address.');
        this.reportValidity();
    } else {
        this.setCustomValidity('');
    }
}

