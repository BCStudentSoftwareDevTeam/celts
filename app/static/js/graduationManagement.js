$(document).ready(function() {
    //var gradStudentsTable = $('#gradStudentsTable').DataTable();
    let selectAllMode = true;
    
    // // Handle filter selection
    // $('.dropdown-item').click(function(e) {
    //     var filterStudents = $(this).attr('href').substring(1); // Get filter type from href attribute (#all, #bonner, #minor)
    //     if (filterStudents === 'all') {
    //         // Show all students
    //         gradStudentsTable.search('').draw();
    //     } else if (filterStudents === 'bonner') {
    //         // Filter for Bonner students
    //         gradStudentsTable.columns(0).search('bonner').draw();
    //     } else if (filterStudents === 'minor') {
    //         // Filter for Minor students
    //         gradStudentsTable.columns(0).search('minor').draw();
    //     }
    //     // Prevent default action
    //     e.preventDefault();

         // Initialize the DataTable
    var table = $('#gradStudentsTable').DataTable();
    // Handle filter selection
    $('.dropdown-item').click(function() {
        var filterType = $(this).data('filter');  // Get the filter type from the data-filter attribute
        if (filterType === 'all') {
            // Show all students
            table.rows().show().draw();
        } else {
            // Filter based on the student type
            table.rows().every(function(rowIdx, tableLoop, rowLoop) {
                var studentType = $(this.node()).data('student-type'); // Get the data-student-type attribute from each row
                if (studentType === filterType) {
                    $(this.node()).show();  // Show the row if it matches the filter
                } else {
                    $(this.node()).hide();  // Hide the row if it doesn't match
                }
            });
            table.draw();
        }
    
    });


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

    //handle filter

    
});
