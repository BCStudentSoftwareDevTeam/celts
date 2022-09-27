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
    new Sortable($('#requirements tbody')[0], {
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
        newrow.find("input").val("")

        newrow.find("select.frequency-select option:first-child").attr('selected', true);
        newrow.find("select:not(.frequency-select) option:last-child").attr('selected', true);

        table.append(newrow)
        addRequirementsRowHandlers()
        newrow.find("input").focus()

        enableSave();
    });

    // Save Requirements handler
    $("#reqSave").click(function() {
        disableSave();
        $.ajax({
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

    // enable the remove button
    $("#requirements button").click(function(e) {
        enableSave();
        $(e.target.closest('tr')).fadeOut(function() { this.remove() });
    });
}

