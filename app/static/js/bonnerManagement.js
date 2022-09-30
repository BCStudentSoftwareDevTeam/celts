import searchUser from './searchUser.js'

$(document).ready(function(){
    $("input[type=search]").on("input", function(){
        let year = $(this).data('year')
        searchUser(this.id, s => cohortRequest(year, "add", s.username), false, null, "student")
    });
    $(".removeBonner").on("click",function(){
        let year = $(this).data('year')
        cohortRequest(year, "remove", $(this).data("username"));
    });

    // Add requirements sorting
    // https://github.com/SortableJS/Sortable
    // https://sortablejs.github.io/Sortable/
    var requirementsObj = new Sortable($('#requirements tbody')[0], {
        animation: 150,
        forceFallback: false,
        handle: '.drag-handle',
        revertOnSpill: true,
        onUpdate: function() {
            enableSave();
        }
    });

    addRequirementsRowHandlers()

    // Add Row handler
    $("#reqAdd").click(function() {
        var table = $("#requirements");
        var newrow = table.find("tbody tr:last-child").clone()
        newrow.data("id", "X");
        newrow.find("input").val("");

        newrow.find("select.frequency-select option:first-child").attr('selected', true);
        newrow.find("select.required-select option:last-child").attr('selected', true);

        table.append(newrow)
        addRequirementsRowHandlers()
        newrow.find("input").focus()

        enableSave();
    });

    // Save Requirements handler
    $("#reqSave").click(function() {
        disableSave();

        var data = $("#requirements tbody tr").map(function(i,row) { 
                        return {
                            'id': $(row).data("id"),
                            'name': $(row).find("input").val(),
                            'required': $(row).find("select.required-select").val() == 'Required' ? true : false,
                            'frequency': $(row).find("select.frequency-select").val() 
                        } 
                    }).get()

        $.ajax({
            'method': 'POST',
            'url': '/saveRequirements/1',
            'contentType': 'application/json',
            'dataType': 'json',
            'data': JSON.stringify(data),
            'success': function(ids) {
                // update our rows with any new ids
                let rows = $('#requirements tbody tr').get()
                ids.forEach(function(id, index) {
                    let row = $(rows[index])
                    if(id != row.data('id')) {
                        row.data('id', id);
                    }
                });
                msgToast("Bonner", "Updated Bonner Requirements");
            }
        });
    });
});

function enableSave() {
    $("#reqSave").attr("disabled", false);
}
function disableSave() {
    $("#reqSave").attr("disabled", true);
}

function cohortRequest(year, method, username){
  $.ajax({
    url: `/bonner/${year}/${method}/${username}`,
    type: "POST",
    success: function(s){
        reloadWithAccordion("cohort-" + year)
    },
    error: function(error, status){
      console.log(error, status)
    }
  })
}

function addRequirementsRowHandlers() {
    // Make the select have a selectable 'empty' value    
    $(".frequency-select").change(function () {
        if(!$(this).val()) {
            $(this).addClass("empty");
        } else {
            $(this).removeClass("empty");
        }
    });
    $(".frequency-select").change();
    $(".frequency-select").change(function(e) {
        enableSave();
    });

    // enable the remove button
    $("#requirements button").click(function(e) {
        enableSave();
        $(e.target.closest('tr')).fadeOut(function() { this.remove() });
    });
    $("#requirements input").keyup(function(e) {
        enableSave();
    });
    $(".required-select").change(function(e) {
        enableSave();
    });
}

