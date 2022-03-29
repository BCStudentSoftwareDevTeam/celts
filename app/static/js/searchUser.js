export default function searchUser(inputId, callback, parentElementId=null, phoneNumber=0){
  var query = $(`#${inputId}`).val()
  $(`#${inputId}`).autocomplete({
    appendTo: (parentElementId === null) ? null : `#${parentElementId}`,
    minLength: 2,
    source: function(request, response) {
      $.ajax({
        url: `/searchUser/${query}/${phoneNumber}`,
        type: "GET",
        dataType: "json",
        success: function(dictToJSON) {
          if (phoneNumber===false){
            response($.map( dictToJSON, function( item ) {
              return {
                label: item,
                value: dictToJSON[item]
              }
            })
          )}
          else {
            response(Object.keys(dictToJSON).map( (item, index) => {
              if (index === 0){
                return {
                  label: item,
                  value: Object.values(dictToJSON)
                }
              }
              else {
                return {
                  label: "",
                  value: ""
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
       $(`#${inputId}`).val("");
       return false;
     }
  });
};
