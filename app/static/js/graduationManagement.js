$(document).ready(function() {
    var gradStudentsTable = $('#gradStudentsTable').DataTable({
        paging: true,
        searching: true,
        info: true
    });

    $("#bonnerDropdown").hide()

    $('.main-dropdown-item').click(function() {
        var filterType = $(this).data('filter'); 
        var buttonText = $(this).text();

        $('#mainFilter').first().text(buttonText);
        $('#cohortFilter').text('Bonner Cohort');

        $('#exportFile').attr('href', `/gradStudentsxls/${filterType}`);

        if (filterType === 'all') {
            $('#bonnerDropdown').hide()

            gradStudentsTable.search('').draw();
            gradStudentsTable.rows().every(function() {
                $(this.node()).show();
            });
            gradStudentsTable.draw(); 
            
        } else if (filterType === 'bonner' ) {
            $('#bonnerDropdown').show()

            filterTable('student-type', "bonner")

        } else if (filterType === 'cce') {
            $('#bonnerDropdown').hide()
            
            filterTable('cce-progress', "True")
        }
    });

    $('.bonner-dropdown-item').click(function() {
        var cohortYear = $(this).data('cohort-year');
        var buttonText = $(this).text();

        $('#cohortFilter').text(buttonText);

        filterTable('cohort-year', cohortYear)
    });

    $('.graduated-checkbox').change(function() {
        let hasGraduated = $(this).is(':checked');
        let username = $(this).data('username');

        $.ajax({
            type: "POST",
            data: {status: hasGraduated ? 1 : 0},
            url: `/${username}/setGraduationStatus`,
            success: function(response) {},
            error: function(status, error) {
                console.error("Error updating graduation status:", error);
            }
        });
    });

    function filterTable(dataFilter, condition) {
        gradStudentsTable.rows().every(function() {
            var data = $(this.node()).data(dataFilter); 
            if (data === condition) {
                $(this.node()).show(); 
            } else {
                $(this.node()).hide();
            }
        });
        gradStudentsTable.draw();
    }
})

