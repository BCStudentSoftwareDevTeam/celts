$(document).ready(function() {
    $('#gradStudentsTable').DataTable();

    $('.graduated-checkbox').change(function() {
        let isChecked = $(this).is(':checked');
        let username = $(this).data('username');
        
        $.ajax({
            type: "POST", 
            url: "/admin/graduationManagement/",
            data: { username: username, hasGraduated: isChecked },
            success: function(response) {
                msgFlash("Graduation status has been updated!", "success");
            },
            error: function(error) {
                msgToast("Error!", "Failed to update graduation status.");
                $(this).prop('checked', !isChecked);  // Revert checkbox state on error
            }
        });
    });
});
