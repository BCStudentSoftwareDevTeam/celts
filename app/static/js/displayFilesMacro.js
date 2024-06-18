$(document).ready(function() {
    $("a.fileName").tooltip();

    $(".removeAttachment").on("click", function() {
        let fileId = $(this).data("id");
        let deleteLink = $(this).data("delete-url");
        let fileData = {
            fileId: fileId,
            databaseId: $(this).data('database-id')
        };

        $.ajax({
            type: "POST",
            url: deleteLink,
            data: fileData,
            success: function() {
                msgFlash("Attachment removed successfully", "success");
                $("#attachment_" + fileId).remove();
            },
            error: function(error) {
                msgFlash(error);
            }
        });
    });

    $('.attachmentCheck').change(function() {
        var attachmentId = $(this).data('id');
        var isChecked = $(this).is(':checked');

        // Uncheck all other checkboxes
        $('.attachmentCheck').not(this).prop('checked', false);

        $.ajax({
            url: '/displayEventFile',
            method: 'POST',
            data: {
                id: attachmentId,
                checked: isChecked
            },
            success: function(response) {
                msgToast("Event Cover", "Successfully updated the event cover.");
            },
            error: function(xhr, status, error) {
                msgFlash(error);
            }
        });
    });
});
