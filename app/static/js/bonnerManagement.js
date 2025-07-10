import searchUser from './searchUser.js'

// add or remove from the Bonner cohort for a particular year
function cohortRequest(year, method, username){
  $.ajax({
    url: `/bonner/${year}/${method}/${username}`,
    type: "POST",
    success: function(s){
        reloadWithAccordion("cohort-" + year)
    },
    error: function(error, status){
    }
  })
}

function downloadSpreadsheet(blob, fileName) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
}

function addSearchCapabilities(inputElement){
    $(inputElement).on("input", function(){
        let year = $(this).data('year');
        searchUser(this.id, student => cohortRequest(year, "add", student.username), false, null, "student");
    }); 
}

function updateExportText(){
    const activeYearElement = document.querySelector(".nav-link.year.active");
    if (!activeYearElement) return;

    const startingYear = Number(activeYearElement.getAttribute("data-year"));
    const newText = `(${startingYear - 5} - ${startingYear})`;
    document.getElementById("last5").textContent = newText;
}

function saveRequirement(e) {
    let el=$(e.target)
    if (el.data("id")== "save-new") {
        $(".saveBtn").removeAttr("disabled");
        let row_el = $("#requirement_" + el.data("id"));
        var row_data = {[el.data("id")]:
                            {
                                'id': row_el.data("id"),
                                'name': row_el.find("input").val(),
                                'required': row_el.find("select.required-select").val() == 'Required' ? true : false,
                                'frequency': row_el.find("select.frequency-select").val()
                            }}
    }
    else {
        let rowid = parseInt(el.data("id"));
        let row_el = $("#requirement_" + rowid);
        var row_data = {[rowid]:
                        {
                            'id': row_el.data("id"),
                            'name': row_el.find("input").val(),
                            'required': row_el.find("select.required-select").val() == 'Required' ? true : false,
                            'frequency': row_el.find("select.frequency-select").val()
                        }}
}
    $.ajax({
        method: 'POST',
        url: '/saveRequirements/1', // Bonner certification id hard-coded here
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(row_data), 

        success: function(ids) {
            msgToast("Bonner", "Updated Bonner Requirements");
            // location.reload();
        },
        error: function(e) {
            msgToast("Error", "Error Saving Requirements");
        }
    });
    
}

/*** Run After Page Load *************************************/
$(document).ready(function(e){
    addRequirementsRowHandlers();
    $("#addCohort").on('click', addCohort);

    $("input[type=search]").each((i, inputElement) => addSearchCapabilities(inputElement));
    $(".removeBonner").on("click", function(){
        let year = $(this).data('year');
        cohortRequest(year, "remove", $(this).data("username"));
    });
    var requirementsObj = new Sortable($('#requirements tbody')[0], {
        animation: 150,
        forceFallback: false,
        handle: '.drag-handle',
        revertOnSpill: true,
        onUpdate: function() {
            enableSave();
        }
    });

    $(".export-spreadsheet").on('click', function() {
        const startingYear = document.getElementsByClassName("nav-link year active")[0].getAttribute("data-year")
        const noOfYears = this.getAttribute("data-years")
        const url = `/bonnerXls/${startingYear}/${noOfYears}`
        let fileName;
        if (noOfYears === "all") {
            fileName = "Bonner Spreadsheet, All Cohorts";
        } else if (Number(noOfYears) === 1) {
            fileName = `Bonner Spreadsheet, ${startingYear} - ${Number(startingYear) + 1}`;
        } else {
            fileName = `Bonner Spreadsheet, ${Number(startingYear) - Number(noOfYears)} - ${startingYear}`;
        }
        $.ajax({
            url: url,
            method: "GET",
            xhrFields: { responseType: "blob" },
            success: function (blob) {
                msgFlash("Download Successful", "success");
                downloadSpreadsheet(blob, fileName);
            },
            error: function (error, status) {
                msgFlash("Download Failed", "danger");
            }
        })
    })
    
    $(".year").on('click', function() {
        updateExportText();
    });

    // Add Requirement handler
    $("#reqAdd").click(function() {
        addRequirement();
    });
});

/** End onready ****************************/

document.addEventListener("DOMContentLoaded", updateExportText);

/* Add a new requirements row and focus it */
function addRequirement() {                            
    var table = $("#requirements");
    var newRow = table.find("tbody tr:last-child").clone();
    newRow.attr('id','requirement_save-new');
    $(newRow).attr("data-id", "save-new");
    newRow.find("input").val("");
    newRow.find("select.frequency-select option:first-child").attr('selected', true);
    newRow.find("select.required-select option:last-child").attr('selected', true);
    newRow.find(".saveBtn").attr('id',"save-new");
    newRow.find(".saveBtn").data('id',"save-new");
    let newSaveBtn = newRow.find(".saveBtn")[0];
    newRow.find("select.frequency-select").attr("name", "frequency-new");
    table.append(newRow)
    // newSaveBtn.addEventListener("click", enableSave());
   
    addRequirementsRowHandlers()
    newRow.find("input").focus()
    $("#reqAdd").attr("disabled", "disabled")
}

function addCohort(){
    // Grab all the cohort years currently displayed
    let years = $('#v-pills-tab .nav-link').map((i, element) => {return Number($(element).data('year'))}).get();
    // Get the latest year from our list and add one
    let newCohortYear = Math.max(...years) + 1;
    // Deselect the currently active tab
    $('#v-pills-tab .active').removeClass('active');
    $('#v-pills-tabContent .tab-pane').removeClass('show active')
    // Add a new (selected) tab to our list of tabs
    $('#v-pills-tab #addCohort').after(`<button class="nav-link active" id="v-pills-${newCohortYear}-tab" data-bs-toggle="pill" data-bs-target="#v-pills-${newCohortYear}" type="button" role="tab" data-year="${newCohortYear}" aria-controls="v-pills-${newCohortYear}" aria-selected="{{aria}}">${newCohortYear} - ${newCohortYear + 1}</button>`)
    // and its corresponding tab pane
    $('#v-pills-tabContent').prepend(`
    <div class="tab-pane fade show active" id="v-pills-${newCohortYear}" role="tabpanel" aria-labelledby="v-pills-${newCohortYear}-tab">
        <div>
            <div class="input-group mb-3">
                <input type="search" id="search-${newCohortYear}" name="search-${newCohortYear}" class="form-control" data-year="${newCohortYear}" placeholder="Add Student" autocomplete="off" style="width:50%" />
                <span class="input-group-text me-1"><span class="bi bi-search"></span></span>
            </div>
            <table class="w-100 table table-striped">
                <tr><td>No students added.</td></tr>
            </table>
        </div>
    </div>`)
    // Add functionality to the search box on the newly added tab
    addSearchCapabilities($(`#search-${newCohortYear}`).get());
}

function addRequirementsRowHandlers() {
    /* Add all of the event handlers to elements in the requirements row.
     *
     * Enable the Save button when there are changes and row additions or removals.
     * Validate the name entry so that they can't submit empty values.
     * Make the frequency select have a selectable default value
     */

    // frequency select styling

    $(".frequency-select").change(function () {
        if(!$(this).val()) {
            $(this).addClass("empty");
        } else {
            $(this).removeClass("empty");
        }
    });

    $(".removebtn").click (function(e) {
        let el = $(e.target)
        let rowid=parseInt(el.data("id"));
        $.ajax({
            method : "POST",
            url: "/deleteReq",
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(rowid), 
            success: function(response) {
                msgToast("Bonner", "Removing Bonner Requirement");
                location.reload();
            },
            error: function(e) {
                msgToast("Error", "Error Removing Requirement");
                location.reload();
            }
        })   
    })

    // handle invalid and valid entries
    $(document).off("click", ".saveBtn").on("click", ".saveBtn", function (e) {
                saveRequirement(e);
    });

    $("#requirements input").on("input blur",function(e) {
        if($(this).val() == "") {
            this.setCustomValidity('Please enter a name.');
            this.reportValidity();
            $(".saveBtn").attr("disabled", "disabled");
        } else {
            $(".saveBtn").removeAttr("disabled");
            this.setCustomValidity('');
            this.reportValidity();
        }
    });

    $("#requirements input").focusout(function(e) {
        if($(this).val() == "") {
            $(this).addClass('invalid');
            $(this).focus()
        }
        else {
            $(this).removeClass('invalid');
            $(this).addClass('valid');
        }
    });
}