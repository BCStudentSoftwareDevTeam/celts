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
        $('#cohortFilter').text('Bonner Cohort');
        


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
            
            var cceUsers = $(this).data('cce'); 

            console.log('Raw string',cceUsers)

            const dataString = `[{'username': 'ayisie', 'firstName': 'Ebenezer', 'lastName': 'Ayisi', 'hasGraduated': False, 'engagementCount': Decimal('2'), 'hasCommunityEngagementRequest': 0, 'hasSummer': 'Incomplete'}, {'username': 'khatts', 'firstName': 'Sreynit', 'lastName': 'Khatt', 'hasGraduated': False, 'engagementCount': Decimal('1'), 'hasCommunityEngagementRequest': 0, 'hasSummer': 'Completed'}, {'username': 'bledsoef', 'firstName': 'Finn', 'lastName': 'Bledsoe', 'hasGraduated': False, 'engagementCount': Decimal('1'), 'hasCommunityEngagementRequest': 0, 'hasSummer': 'Incomplete'}]`;

            // Step 1: Clean the string
            const sanitizedString = dataString
              .replace(/'/g, '"') // Replace single quotes with double quotes
              .replace(/False/g, 'false') // Replace False with false
              .replace(/Decimal\('(\d+)'\)/g, '$1'); // Replace Decimal('x') with x
            
            // Step 2: Initialize the result object
            const result = {};
            
            // Step 3: Split the string into individual user items
            const userItems = sanitizedString.slice(1, -1).split('}, {');
            
            userItems.forEach(item => {
              // Remove curly braces and extra whitespace
              item = item.replace(/[{}/]/g, '').trim();
            
              // Split into key-value pairs
              const pairs = item.split(', ');
            
              let username, engagementCount;
            
              pairs.forEach(pair => {
                const [key, value] = pair.split(': '); // Split into key and value
                if (key.trim() === '"username"') {
                  username = value.replace(/"/g, ''); // Clean username
                } else if (key.trim() === '"engagementCount"') {
                  engagementCount = parseFloat(value); // Convert engagement count to a number
                  console.log('attempt to parse: ',value)
                  
                }
              });
            
              // Add to result if both username and engagementCount were found
              if (username && engagementCount !== undefined) {
                result[username] = engagementCount; // Populate the result object
              }
            });
            
            console.log(result);
            
            


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

        $('#cohortFilter').text(buttonText);
        $('#main-filter').first().text('All');

        // clear table
        gradStudentsTable.rows().every(function(){
            $(this.node()).hide();
        })
        
        console.log(cohortusers)
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

        gradStudentsTable.rows().every(function() {
            // Use jQuery to check visibility
            var rowNode = this.node(); // Get the row node
            if ($(rowNode).is(':visible')) {
                console.log('Row is visible');
            } else {
                console.log('Row is hidden');
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
    // $('#selectAll').click(function() {
    //     let checkboxes = $('.graduated-checkbox');
    //     if (selectAllMode) {
    //         checkboxes.prop('checked', true).change();
    //         $(this).text('Deselect All');
    //     } else {
    //         checkboxes.prop('checked', false).change();
    //         $(this).text('Select All');
    //     }
    //     selectAllMode = !selectAllMode; 
    // });
    

    $('#selectAll').click(function() {

        if (selectAllMode) {
            gradStudentsTable.rows().every(function() {
                // Use jQuery to check visibility
                var rowNode = this.node(); // Get the row node
                if ($(rowNode).is(':visible')) {
                    console.log('Row is visible');
                    $(rowNode).find('.graduated-checkbox').prop('checked', true ).change();
                } 
            });
            $(this).text('Deselect All');
        } else {

            gradStudentsTable.rows().every(function() {
                // Use jQuery to check visibility
                var rowNode = this.node(); // Get the row node
                if ($(rowNode).is(':visible')) {
                    console.log('Row is visible');
                    $(rowNode).find('.graduated-checkbox').prop('checked', false ).change();
                } 
            });
            $(this).text('Select All');
        }
        selectAllMode = !selectAllMode; 
    });
});
