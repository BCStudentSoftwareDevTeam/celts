$(document).ready( function () {

  //make html table to datatable
  var table = $('#SLCProposalTable').DataTable({
   "fnDrawCallback": function(oSettings) {
      if ($('#SLCProposalTable tr').length <= 10) {
         // if entries are less than or equal to 10, there is no need for the dropdown with entries to show.
         $('.dataTables_length').hide();
         //move search box to the left
         $('.dataTables_filter').addClass('float-start');
       }
    }
  });
    $("#downloadApprovedCoursesBtn").click(function(){
        let termID = $("#downloadApprovedCoursesBtn").val();
        $.ajax({
            url:`/serviceLearning/downloadApprovedCourses/${termID}`,
            type:"GET",
            success: function(response){
              callback(response);
            },
            error: function(response){
                console.log(response)
            },


        })
    })
});
