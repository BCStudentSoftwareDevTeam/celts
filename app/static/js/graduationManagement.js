$(document).ready(function() {
    let gradStudentsTable = $('#gradStudentsTable').DataTable({
        paging: true,
        searching: true,
        info: false,
    });
    initializePage()

    $('.main-dropdown-item').click(function() { 
        var filterType = $(this).data('filter'); 

        handleMainFilterChange(filterType) 
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
                initializePage()
                msgFlash(`Saved graduation status for ${username}.`, "success", 1000)
            },
            error: function(status, error) {
                console.error("Error updating graduation status:", error);
                msgFlash(`Error saving graduation status for ${username}.`)
            }
        });
    });

    $('#showGraduatedToggle').click(function() {
        let isToggled = $(this).is(':checked')
        sessionStorage.setItem('showGraduatedToggleState', isToggled ? 1 : 0)
        initializePage()

    })

    function filterTable(dataFilter, condition) {
        gradStudentsTable.rows().every(function() {
            var hasGraduated = $(this.node()).find('input[type="checkbox"]').is(':checked');
            if (!showGraduatedStudents() && (hasGraduated == true)) {
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

    function handleMainFilterChange(filterType) {
        if (filterType == 'cce') {
            var buttonText = 'CCE Minor'
        } else if (filterType == 'bonner') {
            var buttonText = 'Bonner Students'
        } else {
            var buttonText = 'Filter'
        }

        sessionStorage.setItem('mainFilterState', filterType)
        $('#mainFilter').first().text(buttonText);
        $('#cohortFilter').text('Select Cohort');

        $('#exportFile').attr('href', `/gradStudentsxls/${filterType}`);

        if (filterType === 'all') {
            $('#bonnerDropdown').hide()
            sessionStorage.setItem('cohortFilterState', null)

            gradStudentsTable.search('').draw();
            gradStudentsTable.rows().every(function() {
                var hasGraduated = $(this.node()).find('input[type="checkbox"]').is(':checked');
                if (!showGraduatedStudents() && (hasGraduated == true)) {
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
        var showGraduatedToggleState = sessionStorage.getItem('showGraduatedToggleState') || false;
        $('#showGraduatedToggle').prop('checked', Number(showGraduatedToggleState));

        handleMainFilterChange(mainFilterState)

        if (mainFilterState == "bonner") {
            var bonnerButtonText = "All"
            if (cohortFilterState != "all") {
                cohortFilterState = Number(cohortFilterState) 
                bonnerButtonText = `${cohortFilterState}-${cohortFilterState+1}`
            }
            handleBonnerFilterChange(cohortFilterState, bonnerButtonText)
        }
    }

    function showGraduatedStudents() {
        return $('#showGraduatedToggle').is(':checked') 
    }
})

