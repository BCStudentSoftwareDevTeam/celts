export default function searchUser(inputId, ajaxUrl, formId){
  var query = $(`#${inputId}`).val()

  $(`#${inputId}`).autocomplete({
    minLength: 2,
    source: function(request, response){

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
       $(`#${formId}`).submit()
     }
  });
};
