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

        $('#main-filter').first().text(buttonText);

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

        var cohortusers = $(this).data('cohort-users');
        var buttonText = $(this).text();

        $('.dropdown-toggle.bonner-filter').text(buttonText);

        // clear table
        gradStudentsTable.rows().every(function(){
            $(this.node()).hide();
        })

        //Make list of users from cohort users

        const cleanedString = cohortusers
            .replace(/^\[|\]$/g, '') // Remove the square brackets
            .replace(/<User:\s*|>/g, '') // Remove "<User: " and ">"
            .trim(); // Trim any leading or trailing whitespace

        const CohortArray = cleanedString.split(',').map(user => user.trim());

        //if list isnt empty then add users on list        
        gradStudentsTable.rows().every(function() {
            var studentUserName = $(this.node()).data('username');

            for ( let i = 0 ; i < CohortArray.length ; i++){
                
                var studentType = $(this.node()).data('student-type'); 
                if (studentType === 'bonner' && studentUserName == CohortArray[i]) {
                    $(this.node()).show(); 
                    { break; }
                } else {
                    $(this.node()).hide();
                }
            }         
        });
 
        gradStudentsTable.draw();
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
