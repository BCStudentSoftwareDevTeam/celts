export default function searchUser(inputId, callback, clear=false, parentElementId=null, category = null)
{
  $(`#${inputId}`).autocomplete({
    appendTo: (parentElementId === null) ? null : `#${parentElementId}`,
    minLength: 2,
    source: function(request, response) {      
      $.ajax({
        url: `/searchUser/${request.term}`,   // use the live term
        type: "GET",
        dataType: "json",
        data: {"category": category},
        success: function(searchResults) {
          response(Object.entries(searchResults).map((item) => {
            return {
              label: (item[1]["firstName"] + " " + item[1]["lastName"] + " (" + item[0] + ")"),
              value: item[1]["username"],
              dictvalue: item[1],
            }
          }))
        },
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
    },
    autoFocus: true
  });
};