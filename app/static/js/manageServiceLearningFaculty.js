$(document).ready( function () {

  //make html table to datatable
   var table =  $('#myTable').DataTable({
   "fnDrawCallback": function(oSettings) {
     if ($('#myTable tr').length <= 10) {
         // if entries are less than or equal to 10, there is no need for the dropdown with entries to show.
         $('.dataTables_length').hide();
         //move search box to the left
         $('.dataTables_filter').addClass('float-start');
       }
    }
  });
    $("#sendRecommendationBtn").click(function(){
        let termID = $("#sendRecommendationBtn").val();
        $.ajax({
            url:`/serviceLearning/sendRecommendation/${termID}`,
            type:"GET",
            success: function(response){
                console.log(response)
            },
            error: function(response){
                console.log(response)
            },


        })
    })
});
