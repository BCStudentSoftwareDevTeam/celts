$(document).ready(function(){
    $("#removeRsvpBtn").click(function(){
        removeRsvpForEvent($("#removeRsvpBtn").val())
    })
    $("#rsvpBtn").click(function(){
        rsvpForEvent($("#rsvpBtn").val())
    })
    $("#toggleButton").on("click", toggleButton)
})

function rsvpForEvent(eventID){
  rsvpInfo = {id: eventID,
              from: 'ajax'}

  $.ajax({
    url: "/rsvpForEvent",
    type: "POST",
    data: rsvpInfo,
    success: function(s){
        location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }
  });
}

function removeRsvpForEvent(eventID){
  removeRsvpInfo = {id: eventID,
                    from: 'ajax'}

  $.ajax({
    url: "/rsvpRemove",
    type: "POST",
    data: removeRsvpInfo,
    success: function(s){
        location.reload()
    },
    error: function(error, status){
        console.log(error, status)
    }

  })
}


$(document).ready(function(){
  localStorage.removeItem("toggleState");
  var toggleButton = $("#toggleButton");
  toggleButton.prop("checked", false);
  toggleRows(false)

  toggleButton.on("change", function(){
    var isChecked = $(this).prop("checked");
    toggleRows(isChecked)

    localStorage.setItem("toggleState", isChecked ? "checked" : "unchecked")
  });
  function toggleRows(isChecked) {
    var tableRows = $(".showlist");
    if (isChecked){
      tableRows.removeClass("d-none");
    }
    else{
      tableRows.addClass("d-none")
    }
  }
})


// function toggleButton(){
  
  

//   if (toggleButton.is(":checked")){
//     tableRows.each(function() {
//       var tableRow = $(this);
//       if (tableRow.hasClass("d-none")) {
//         tableRow.removeClass("d-none");
//       }
//     });
//   }

//   else {
//     tableRows.each(function() {
//       var tableRow= $(this);
//       if(!tableRow.hasClass("d-none")) {
//         tableRow.addClass("d-none");
//       }
//     });
//   }
// }

