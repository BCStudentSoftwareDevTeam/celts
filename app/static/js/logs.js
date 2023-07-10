$(document).ready(function() {
    $('#logsTable').DataTable({ "order": [[ 0, "desc" ]] });
    $('#logsTable').removeClass("d-none");
    $('#logsTable').DataTable().columns.adjust().draw()
  });
