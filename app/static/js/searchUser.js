export default function searchUser(inputId, callback, clear=false, parentElementId=null, category = null)
{
  var query = $(`#${inputId}`).val()
  let columnDict = {};
  $(`#${inputId}`).autocomplete({
    appendTo: (parentElementId === null) ? null : `#${parentElementId}`,
    minLength: 2,
    source: function(request, response) {
      $.ajax({
        url: `/searchUser/${query}`,
        type: "GET",
        dataType: "json",
        data:{"category":category},
        success: function(searchResults) {
          response(Object.entries(searchResults).map( (item) => {
              return {
                // label: firstName lastName (username)
                // value: username
                label: (item[1]["firstName"]+" "+item[1]["lastName"]+" ("+item[0]+")"),
                value: item[1]["username"],
                dictvalue: item[1],
              }
          }
        ))},
        error: function(request, status, error) {
          console.log(status, error);
        }
      })
    },
     select: function(event, ui) {
       $(`#${inputId}`).val(ui.item.value);
       callback(ui.item.dictvalue);
       if(clear){
         $(`#${inputId}`).val("");
        }

       return false;
     }
  });
};
