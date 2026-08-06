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
    // signaturePad.clear(); 
}

window.addEventListener("resize", resizeCanvas);

$('#editVolunteerModal').on('shown.bs.modal', function () {
    resizeCanvas();    
});

$('#editVolunteerModal').on('hidden.bs.modal', function () {
    if (!signaturePad.isEmpty() & hasSavedSignature) {
        $("#signatureHeader").remove();
        canvas.remove();
        // signaturePad.clear();
        $("#signatureButtons").hide();
    }
});

$('#clear-btn').on('click', function () {
    signaturePad.clear();
});

var hasSavedSignature = false;

$('#save-btn').on('click', function () {    
    if (signaturePad.isEmpty()) {
        alert("You forgot to sign!");   
    } else {
        $.ajax({
            url: `/handbookSignature`,
            type: "POST",
            headers: {'Content-Type': 'application/json'},
            data: {studentUsername: $('#handbook-signature-pad').data('student')},
            success: function(s){            
                signaturePad.off();
                $("#signatureConfirmation").show();
                $("#signatureButtons").hide();
                const today = new Date();
                $("#signatureText").text("CELTS Handbook signed for AY 2026-2027");
                $("#signatureText").css("color", "black");
                $("#handbookSignatureContainer .bi-info-circle-fill").hide();
                hasSavedSignature = true;
            },
            error: function(error, status){
                console.log(error, status)
                $("#signatureConfirmation h3").text("Uh oh. Something wrong. Please seek out help from the CELTS staff")
                $("#signatureConfirmation h3").replaceWith(function() {
                    return $('<p>', { html: $(this).html() });
                });
                $("#signatureConfirmation").show();
                $("#signatureButtons").hide();
            }
        })
    }
});
