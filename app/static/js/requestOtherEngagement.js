$(document).ready(function(){
    handleFileSelection("attachmentObject")
    
    $('#weekInput').on('keypress', function(event) {
        var charCode = event.which;
        if (!(charCode >= 48 && charCode <= 57) && charCode !== 8) {
            event.preventDefault();
            $('#errorMessage').display();
        } else {
            $('#errorMessage').text('');
        }
    });
    
    $('#timeInput').on('input', function() {
        validateFloatInput($(this));
    });
    
    $("#sendOtherRequest").on("click", function() {
        submitOtherCommEngReq()
              
  })
    
});

function validateFloatInput(input) {
    var inputValue = input.val();
    var floatRegex = /^ *-?\d+(\.\d+)? *$/;
    if (!floatRegex.test(inputValue)) {
        input.addClass('invalid');
        input.preventDefault();
    } else {
        input.removeClass('invalid');
    }
}

function submitOtherCommEngReq(){
    var formData = $("from").serialize()
    $.ajax({
            url: "/cceMinor/"+username+"/requestOtherCommunityEngagement",
            type: "GET",
            data: data,
            success: alert,
            error: function(request, status, error) {
                    msgFlash("Error saving changes!", "danger")
                }
            });
}