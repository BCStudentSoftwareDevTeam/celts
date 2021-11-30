$(document).ready( function () {
  //make html table to datatable
   var table =  $('#myTable').DataTable({
   "fnDrawCallback": function(oSettings) {
     if ($('#myTable tr').length < 11) {
         $('.dataTables_length').hide();
         //move search box to the left
         $('.dataTables_filter').addClass('float-start');
       }
    }
  });
});
