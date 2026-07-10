var canvas = $('#handbook-signature-pad')[0];
var signaturePad = new SignaturePad(canvas);

// Resize canvas to fix Bootstrap 3 responsiveness
function resizeCanvas() {
    var ratio =  Math.max(window.devicePixelRatio || 1, 1);
    canvas.width = canvas.offsetWidth * ratio;
    canvas.height = canvas.offsetHeight * ratio;
    canvas.getContext("2d").scale(ratio, ratio);
    signaturePad.clear(); // Clear it out to accommodate the new size
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();

// Button Actions
$('#clear-btn').on('click', function () {
    signaturePad.clear();
});


$('#save-btn').on('click', function () {   
    console.log(":"+$('#searchStudentsInput').val()+":") 
    if (!$('#searchStudentsInput').val())  {
        alert("Select a student!")    
    } else if ($('.checkbox:checked').length != $('.checkbox').length)  {
        alert("Please read and agree to all the statements.")    
    } else if (signaturePad.isEmpty()) {
        alert("Please provide a signature first.");            
    } else {
        var dataURL = signaturePad.toDataURL();
        console.log(dataURL); // You can send this base64 string to your server
        alert("Thank you for signing the CELTS Handbook. We look forward to your participation in CELTS!");
        $.ajax({
            url: `/handbookSignature`,
            type: "POST",
            data: {studentID: $('#handbook-signature-pad').attr('data-student')},
            success: function(s){
                console.log("Saved!")
            },
            error: function(error, status){
                console.log(error, status)
            }
        })
    }
});

var searchResult = null;
import searchUser from './searchUser.js'
function callback(selected) {
  // don't do anything with the search results
}

$(document).ready(function() {
    $("#searchStudentsInput").on("input", function() {
        searchResult = searchUser("searchStudentsInput", callback);
    });
    
    $("#searchStudentsInput").change(function() {
        $('#handbook-signature-pad').attr('data-student',  $(this).val());
    });

    $(".checkboxes").on("change", function() {        
        if ($('.checkbox:checked').length === $('.checkbox').length) {
            $('#handbook-signature-pad').removeClass("disabled");
        } else {
            $('#handbook-signature-pad').addClass("disabled");
            signaturePad.clear();
        }
    });
  
    
});