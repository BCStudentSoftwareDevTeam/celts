export default function searchUser(inputId, callback, clear=false, parentElementId=null, columnRequested=null, user){
  var query = $(`#${inputId}`).val()

  let columnDict={};
  console.log(user)
  $(`#${inputId}`).autocomplete({
    appendTo: (parentElementId === null) ? null : `#${parentElementId}`,
    minLength: 2,
    
    source: function(request, response) {
      
      $.ajax({
        url: `/searchUser/${query}`,
        type: "GET",
        data:{"searchvalue":user},
        dataType: "json",
        // data:{"user1":user},
        success: function(searchResults) {
          response(Object.entries(searchResults).map( (item) => {
            if (!columnRequested){
              return {
                // label: firstName lastName (username)
                // value: username
                label: (item[1]["firstName"]+" "+item[1]["lastName"]+" ("+item[0]+")"),
                value: item[0]
              }
            } else {
              for (const column of columnRequested) {
                columnDict[column]=item[1][column];
              };
              return {
                // label: firstName lastName (username)
                // value: "{column: response, column2: response2, ...}"
                // must JSON.parse
                label: (item[1]["firstName"]+" "+item[1]["lastName"]+" ("+item[0]+")"),
                value: JSON.stringify(columnDict)
              }
            }
          }
        ))},
        error: function(request, status, error) {
          console.log(status, error);
        }
      })
    },
     select: function(event, ui) {
       var user = ui.item.value
       $(`#${inputId}`).val(ui.item.value);
       callback();
       if(clear){
       $(`#${inputId}`).val("");
       return false;
     }
     }
  });
};
