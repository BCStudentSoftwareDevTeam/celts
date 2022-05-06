export default function searchUser(searchOptions){
  // inputId, callback,clear=false,group="default", parentElementId=null, columnRequested=null
  var defaultOptions = {
    clear:false,
    group:"default",
    parentElementId:null,
    columnRequested:null,
  };

  for (var key in defaultOptions){
    if (searchOptions.hasOwnProperty(key) == false){
      searchOptions[key] = defaultOptions[key];
    }
  }

  var query = $(`#${searchOptions.inputId}`).val();
  let columnDict={};
  $(`#${searchOptions.inputId}`).autocomplete({
    appendTo: (searchOptions.parentElementId === null) ? null : `#${searchOptions.parentElementId}`,
    minLength: 2,
    source: function(request, response) {
      $.ajax({
        url: `/searchUser/${query}/${searchOptions.group}`,
        type: "GET",
        dataType: "json",
        success: function(searchResults) {
          response(Object.entries(searchResults).map( (item) => {
            if (!searchOptions.columnRequested){
              return {
                // label: firstName lastName (username)
                // value: username
                label: (item[1]["firstName"]+" "+item[1]["lastName"]+" ("+item[0]+")"),
                value: item[0]
              }
            } else {
              for (const column of searchOptions.columnRequested) {
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
       $(`#${searchOptions.inputId}`).val(ui.item.value);
       searchOptions.callback();
       if(clear){
       $(`#${searchOptions.inputId}`).val("");
       return false;
     }
     }
  });
};
