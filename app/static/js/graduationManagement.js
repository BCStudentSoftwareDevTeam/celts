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

        $('.dropdown-toggle').text(buttonText);

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

        var BfilterType = $(this).data('newfilter');
        var year = $(this).text();

        year = year.substring(0,4)

        msgFlash(year)

        year = Integer.parseInt(year);




        if (BfilterType === 'bonnercohort') {
            gradStudentsTable.rows().every(function() {
                var studentType = $(this.node()).data('student-type'); 
                if (studentType === 'bonnercohort') {
                    $(this.node()).show(); 
                } else {
                    $(this.node()).hide();
                }
            });
            gradStudentsTable.draw();


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
        selectAllMode = !selectAllMode; 
    });
    
});
