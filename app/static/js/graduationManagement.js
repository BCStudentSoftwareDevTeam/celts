$(document).ready(function() {
    $('#gradStudentsTable').DataTable();
    let selectAllMode = true;

    $('.graduated-checkbox').change(function() {
        let hasGraduated = $(this).is(':checked');
        let username = $(this).data('username');
        let routeUrl = hasGraduated ? "hasGraduated" : "hasNotGraduated";
        let graduationURL = "/" + username + "/" + routeUrl + "/"

        $.ajax({
            type: "POST", 
            url: graduationURL,
            success: function(response) {
                msgFlash("Graduation status updated successfully!", "success")
                console.log("Graduation status updated successfully!");
            },
            error: function(status, error) {
                msgFlash("Graduation status updated successfully!", "error")
                console.error("Error updating graduation status:", error);
            }
        });
    });
    $('#selectAll').click(function() {
        let checkboxes = $('.graduated-checkbox');
        if (selectAllMode) {
            checkboxes.prop('checked', true).change();
            $(this).text('Deselect All');
        } else {
            checkboxes.prop('checked', false).change();
            $(this).text('Select All');
        }
        selectAllMode = !selectAllMode; // Toggle the state
    });
});
