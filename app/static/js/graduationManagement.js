$(document).ready(function() {
    var gradStudentsTable = $('#gradStudentsTable').DataTable({
        paging: true,
        searching: true,
        info: true
    });
    let selectAllMode = true;
    
    $('.dropdown-item').click(function() {
        var filterType = $(this).data('filter'); 
        var buttonText = $(this).text();

        $('.dropdown-toggle').first().text(buttonText);

        if (filterType === 'all') {
            gradStudentsTable.search('').draw();
            gradStudentsTable.rows().every(function() {
                $(this.node()).show();  
            });
            gradStudentsTable.draw(); 
            
        } else if (filterType === 'bonner' )  {
            gradStudentsTable.rows().every(function() {
                var studentType = $(this.node()).data('student-type'); 
                if (studentType === 'bonner') {
                    $(this.node()).show(); 
                } else {
                    $(this.node()).hide();
                }
            });
            gradStudentsTable.draw();
        
        } else if (filterType === 'cce') {
            gradStudentsTable.rows().every(function() {
                var studentType = $(this.node()).data('student-type'); 
                if (studentType === 'cce') {
                    $(this.node()).show(); 
                } else {
                    $(this.node()).hide();
                }
            });
            gradStudentsTable.draw();
        
        }
    });

    $('.dropdown-item-new').click(function() {
        
        var cohortYear = $(this).data('cohort-year');
        var buttonText = $(this).text();

        $('.dropdown-toggle.bonner-filter').text(buttonText);
        
        gradStudentsTable.rows().every(function() {
            var studentYear = $(this.node()).data('cohort-year');
            if (studentYear == cohortYear) {
                $(this.node()).show(); 
            } else {
                $(this.node()).hide();
            }
        });
        gradStudentsTable.draw();

        $('.dropdown-menu .dropdown-item-new').each(function() {
            var itemYear = $(this).data('cohort-year');
            if (itemYear == cohortYear) {
              $(this).addClass('active');
            } else {
              $(this).removeClass('active');
            }
        });
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
        selectAllMode = !selectAllMode; 
    });
    
});
