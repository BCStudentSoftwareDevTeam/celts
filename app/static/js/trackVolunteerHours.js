// function searchVolunteer(){
// var query = $("#volunteerInput").val()
// $("#volunteerInput").autocomplete({
//   minLength: 2,
//   source: function(request, response){
//     $.ajax({
//       url: "/searchVolunteers/" + query,
//       type: "GET",
//       contentType: "application/json",
//       data: query,
//       dataType: "json",
//       success: function(dictToJSON) {
//         response($.map( dictToJSON, function( item ) {
//           return {
//             label: item,
//             value: dictToJSON[item]
//         }
//       }))
//     },
//       error: function(request, status, error) {
//         console.log(status,error);
//       }
//     })
//   },
//   select: function( event, ui ) {
//     var volunteerName = ui.item.value
//     $("#Volunteertable").append('<tr><td>' + volunteerName + '</td><td><button id="removeButton" onclick="removeRow(this)" type="button">x</button></td></tr>')
//
//     }
//   });
// };
