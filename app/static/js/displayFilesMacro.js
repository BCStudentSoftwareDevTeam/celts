$(document).ready(function(){
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
                msgFlash("Attachment removed successfully")
                $("#attachment_"+fileId).remove()
        
            },
                error: function(error){
                    msgFlash(error)
            }
            });
        });
})
