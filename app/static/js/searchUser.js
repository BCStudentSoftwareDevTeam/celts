export default function searchUser(inputId, callback, parentElementId=null, object=false){
  var query = $(`#${inputId}`).val()
  $(`#${inputId}`).autocomplete({
    appendTo: (parentElementId === null) ? null : `#${parentElementId}`,
    minLength: 2,
    source: function(request, response) {
      $.ajax({
        url: `/searchUser/${query}/${object}`,
        type: "GET",
        dataType: "json",
        success: function(dictToJSON) {
          if (object===false){
            response($.map( dictToJSON, function( item ) {
              return {
                label: item,
                value: dictToJSON[item]
              }
            })
          )}
          else {
            response(Object.keys(dictToJSON).map( (item, index) => {
              if (index ===0){
                return {
                  label: item,
                  value: dictToJSON[item]
                }
              }
            })
          )}
        },
        error: function(request, status, error) {
          console.log(status, error);
        }
      })
    },
     select: function(event , ui) {
       var user = ui.item.value
       $(`#${inputId}`).val(ui.item.value);
       callback();
     }
  });
};
