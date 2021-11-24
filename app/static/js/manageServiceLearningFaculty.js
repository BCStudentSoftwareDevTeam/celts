$(document).ready( function () {
   var table =  $('#myTable').DataTable({
   "fnDrawCallback": function(oSettings) {
     if ($('#myTable tr').length < 11) {
         $('.dataTables_length').hide();
         $('.dataTables_filter').addClass('float-start');
       }
    }
  });
});
