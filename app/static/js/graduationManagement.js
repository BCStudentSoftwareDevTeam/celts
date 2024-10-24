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

        $('#selectAll').text('Select All');
        selectAllMode = true

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

            const sanitizedString = cceUsers
              .replace(/'/g, '"') 
              .replace(/False/g, 'false') 
              .replace(/Decimal\('(\d+)'\)/g, '$1'); 
            
            const CCElist = {};
            
            const userItems = sanitizedString.slice(1, -1).split('}, {');
            
            userItems.forEach(item => {
  
              item = item.replace(/[{}/]/g, '').trim();
            

              const pairs = item.split(', ');
            
              let username, engagementCount;
            
              pairs.forEach(pair => {
                const [key, value] = pair.split(': '); 
                if (key.trim() === '"username"') {
                  username = value.replace(/"/g, '');
                } else if (key.trim() === '"engagementCount"') {
                  engagementCount = parseFloat(value[9]); 
                  
                }
              });
            
              
              if (username && engagementCount !== undefined) {
                CCElist[username] = engagementCount; 
              }
            });
            

            gradStudentsTable.rows().every(function() {
                var studentUserName = $(this.node()).data('username');
                
                for ( const [key, value] of Object.entries(CCElist)){
                    var username = key;
                    
                    if ( studentUserName == username && CCElist[key] > 0 ) {
                        $(this.node()).show(); 
                        { break; }
                    } else {
                        $(this.node()).hide();
                    }
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

        $('#selectAll').text('Select All');
        selectAllMode = true

        gradStudentsTable.rows().every(function(){
            $(this.node()).hide();
        })
        

        const cleanedString = cohortusers
            .replace(/^\[|\]$/g, '') 
            .replace(/<User:\s*|>/g, '') 
            .trim(); 

        const CohortArray = cleanedString.split(',').map(user => user.trim());

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

        if (selectAllMode) {
            gradStudentsTable.rows().every(function() {
                var rowNode = this.node(); 
                if ($(rowNode).is(':visible')) {
                    $(rowNode).find('.graduated-checkbox').prop('checked', true ).change();
                } 
            });
            $(this).text('Deselect All');
        } else {

            gradStudentsTable.rows().every(function() {
                var rowNode = this.node(); 
                if ($(rowNode).is(':visible')) {
                    $(rowNode).find('.graduated-checkbox').prop('checked', false ).change();
                } 
            });
            $(this).text('Select All');
        }
        selectAllMode = !selectAllMode; 
    });
});
