$(document).ready(function(){
    $("a.fileName").tooltip()
    $(".removeAttachment").on("click", function(){
        let fileId=  $(this).data("id")
        let deleteLink = $(this).data("delete-url")
        let fileData = {fileId : fileId,
                        databaseId:$(this).data('database-id')}
        $.ajax({
            type:"POST",
            url: deleteLink,
            data: fileData, //get the startDate, endDate and name as a dictionary
            success: function(){
                msgFlash("Attachment removed successfully", "success")
                $("#attachment_"+fileId).remove()
        
            },
                error: function(error){
                    msgFlash(error)
            }
            });
        });

    $('.attachmentCheck').change(function() {
        // Store the current checkbox state
        var isChecked = $(this).is(':checked');
        
        // Uncheck all checkboxes
        $('.attachmentCheck').prop('checked', false);
        
        // If the current checkbox was previously unchecked, check it
        if (!isChecked) {
            $(this).prop('checked', true);
        } else {
            $(this).prop('checked', false);
        }

        var attachmentId = $(this).data('id');
        var isChecked = $(this).is(':checked');


        $.ajax({
            url: '/displayEventFile',
            method: 'POST',
            data: {
                id: attachmentId,
                checked: isChecked
            },
            success: function(response) {
                msgToast("Event Cover ", "Successfully updated the event cover.")
            },
            error: function(xhr, status, error) {
                msgFlash(error)
                
            }
        });
    });

    
          
})

