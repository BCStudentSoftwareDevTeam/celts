var canvas = $('#handbook-signature-pad')[0];
var signaturePad = new SignaturePad(canvas);

// Resize canvas to fix Bootstrap 3 responsiveness
function resizeCanvas() {
    var ratio = Math.max(window.devicePixelRatio || 1, 1);
    var displayWidth = canvas.offsetWidth;
    var displayHeight = canvas.offsetHeight;
    canvas.width = displayWidth * ratio;
    canvas.height = displayHeight * ratio;
    // Lock the on-page size so it doesn't visually grow with the buffer
    canvas.style.width = displayWidth + "px";
    canvas.style.height = displayHeight + "px";
    canvas.getContext("2d").scale(ratio, ratio);
    signaturePad.clear(); 
}

window.addEventListener("resize", resizeCanvas);

$('#editVolunteerModal').on('shown.bs.modal', function () {
    resizeCanvas();
});

$('#editVolunteerModal').on('hidden.bs.modal', function () {
    $("#signatureHeader").remove();
    canvas.remove();
});

$('#clear-btn').on('click', function () {
    signaturePad.clear();
});


$('#save-btn').on('click', function () {    
    $.ajax({
        url: `/handbookSignature`,
        type: "POST",
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({studentID: $('#handbook-signature-pad').attr('data-student')}),
        success: function(s){
            alert("Thank you for signing the CELTS Handbook. We look forward to your participation in CELTS!");
            signaturePad.off();
            $('#save-btn').hide();
            $('#clear-btn').hide();
            const today = new Date();
            $("#signatureDate").text(today.toLocaleDateString('en-US'));
            $("#signatureDate").css("color", "black");
            $("#handbookSignatureContainer .bi-info-circle-fill").hide();
        },
        error: function(error, status){
            console.log(error, status)
        }
    })    
});