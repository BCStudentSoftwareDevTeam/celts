$(document).ready(function() {
    $('#engagedStudentsTable').DataTable({ "order": [[ 0, "desc" ]] });
    $('#engagedStudentsTable').DataTable().columns.adjust().draw();

    $('#interestedStudentsTable').DataTable({ "order": [[ 0, "desc" ]] });
    $('#interestedStudentsTable').DataTable().columns.adjust().draw();

  });


