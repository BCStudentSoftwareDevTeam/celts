export default function searchUser(inputId, callback, parentElementId=null){
  var query = $(`#${inputId}`).val()

  $(`#${inputId}`).autocomplete({
    appendTo: (parentElementId === null) ? null : `#${parentElementId}`,
    minLength: 2,
    source: function(request, response) {
      $.ajax({
        url: `/searchUser/${query}`,
        type: "GET",
        dataType: "json",
        success: function(dictToJSON) {
          response($.map( dictToJSON, function( item ) {
            return {
              label: item,
              value: dictToJSON[item]
            }
          }))
        },
        error: function(request, status, error) {
          console.log(status, error);
        }
      })
    },
     select: function(event , ui) {
       var user = ui.item.value
       $(`#${inputId}`).val(ui.item.value)
       callback();
     }
  });
};
