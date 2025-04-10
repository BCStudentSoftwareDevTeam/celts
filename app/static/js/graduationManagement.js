$(document).ready(function() {
    let gradStudentsTable = $('#gradStudentsTable').DataTable({
        paging: true,
        searching: true,
    });
    initializePage()

    $('.main-dropdown-item').click(function() { 
        var filterType = $(this).data('filter'); 
        var buttonText = $(this).text();
        console.log(buttonText)

        handleMainFilterChange(filterType, buttonText) 
    });

    $('.bonner-dropdown-item').click(function() {
        var cohortYear = $(this).data('cohort-year');
        var buttonText = $(this).text();

        handleBonnerFilterChange(cohortYear, buttonText)
    });

    $('.graduated-checkbox').change(function() {
        let hasGraduated = $(this).is(':checked');
        let username = $(this).data('username');

        $.ajax({
            type: "POST",
            data: {status: hasGraduated ? 1 : 0},
            url: `/${username}/setGraduationStatus`,
            success: function(response) {
                location.reload()
            },
            error: function(status, error) {
                console.error("Error updating graduation status:", error);
                location.reload()
            }
        });
    });

    $('#showGraduatedToggle').click(function() {
        let isToggled = $(this).is(':checked')
        sessionStorage.setItem('showGraduatedToggleState', isToggled ? 1 : 0)
        location.reload()
    })

    function filterTable(dataFilter, condition) {
        gradStudentsTable.rows().every(function() {
            var hasGraduated = $(this.node()).data("has-graduated"); 
            if (!showGraduatedStudents() && (hasGraduated == "True")) {
                $(this.node()).hide();
                return 
            }
            var data = $(this.node()).data(dataFilter); 

            if (data === condition) {
                $(this.node()).show(); 
            } else {
                $(this.node()).hide();
            }
        });
        gradStudentsTable.draw();
    }

    function handleBonnerFilterChange(cohortYear, buttonText) {
        $('#cohortFilter').text(buttonText);
        sessionStorage.setItem('cohortFilterState', cohortYear)

        if (cohortYear == "all") {
            filterTable('student-type', "bonner")
            return
        }

        filterTable('cohort-year', cohortYear)
    }

    function handleMainFilterChange(filterType, buttonText) {
        sessionStorage.setItem('mainFilterState', filterType)
        $('#mainFilter').first().text(buttonText);
        $('#cohortFilter').text('Select Cohort');

        $('#exportFile').attr('href', `/gradStudentsxls/${filterType}`);

        if (filterType === 'all') {
            $('#bonnerDropdown').hide()
            sessionStorage.setItem('cohortFilterState', null)

            gradStudentsTable.search('').draw();
            gradStudentsTable.rows().every(function() {
                var hasGraduated = $(this.node()).data("has-graduated"); 
                if (!showGraduatedStudents() && (hasGraduated == "True")) {
                    $(this.node()).hide();
                    return 
                }
                $(this.node()).show();
            });
            gradStudentsTable.draw(); 
            
        } else if (filterType === 'bonner' ) {
            $('#bonnerDropdown').show()
            sessionStorage.setItem('cohortFilterState', 'all')

            filterTable('student-type', "bonner")

        } else if (filterType === 'cce') {
            $('#bonnerDropdown').hide()
            sessionStorage.setItem('cohortFilterState', null)
            
            filterTable('cce-progress', "True")
        }
    }

    function initializePage() {
        var mainFilterState = sessionStorage.getItem('mainFilterState') || 'all';
        var cohortFilterState = sessionStorage.getItem('cohortFilterState') || 'all';
        console.log(cohortFilterState)
        var showGraduatedToggleState = sessionStorage.getItem('showGraduatedToggleState') || false;

        if (mainFilterState == 'cce') {
            var buttonText = 'CCE Minor'
        } else if (mainFilterState == 'bonner') {
            var buttonText = 'Bonner Students'
        } else {
            buttonText = 'Filter'
        }
        handleMainFilterChange(mainFilterState, buttonText)

        if (mainFilterState == "bonner") {
            var bonnerButtonText = "All"
            if (cohortFilterState != "all") {
                cohortFilterState = Number(cohortFilterState) 
                bonnerButtonText = `${cohortFilterState}-${cohortFilterState+1}`
            }
            handleBonnerFilterChange(cohortFilterState, bonnerButtonText)
        }
        $('#showGraduatedToggle').prop('checked', Number(showGraduatedToggleState));
    }

    function showGraduatedStudents() {
        return $('#showGraduatedToggle').is(':checked') 
    }
})

