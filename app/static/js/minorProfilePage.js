import { validateEmail } from "./emailValidation.mjs";

$(document).ready(function() {
  $("#supervisorEmail").on('input', validateEmail);

  $('input.phone-input').inputmask('(999)-999-9999')
  $('input.phone-input').on('input', function(){
      let matches = $(this).val().match(/\d/g);
      let digits = matches?matches.length:0;
      if (digits == 0 || digits == 10){
          this.setCustomValidity('')

      }
      else{
          this.setCustomValidity('Please enter a valid phone number.')    
          this.reportValidity()        
      }
  })

  handleFileSelection("supervisorAttachment", true)

  $('.submit-proposal').on('click', function(e) {
    e.preventDefault();
    let status = $(this).data('status');
    $('#statusField').val(status);
    
    if (!$('#proposalForm')[0].checkValidity()) {
      $('#proposalForm')[0].reportValidity();
      const stats= $('#statusField').val();
      console.log(stats)
      const form = $('#proposalForm')[0];
      if(stats ==="Submitted"){
        const firstInvalid = form.querySelector(':invalid');
      if (firstInvalid && stats ==="Submitted") {
        firstInvalid.scrollIntoView({
          block: 'center' });
          firstInvalid.focus();

         }
     
      // $( '#proposalForm').submit()
      return;
      }

      
    }    
    var formData = new FormData($('#proposalForm')[0]);
    var actionURL = $('#proposalForm').attr('action');
    let username = $("#username").val();
    
    $.ajax({
      url: actionURL,
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        window.location.href = `/profile/${username}/cceMinor?tab=manageProposals`;
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
  });

  $('#exitButton').on('click', function() {
    let username = $("#username").val()
    window.location.href = `/profile/${username}/cceMinor?tab=manageProposals` 
  }) 

  // ************** SUSTAINED COMMUNITY ENGAGEMENTS ************** //
  $('.engagement-row').on("click", function() {
    showEngagementInformation($(this).data('engagement-data'));
  });
  $('.engagement-row input').on("click", function(e) {
      e.stopPropagation()

      let engagementData = $(this).parents('.engagement-row').data('engagement-data');
    
      toggleEngagementCredit($(this).is(':checked'), engagementData, this)
  });

  // ************** END SUSTAINED COMMUNITY ENGAGEMENTS ************** //

  // ************** SUMMER EXPERIENCE ************** //
  $('#hoursBelow300Container').hide()
  toggleUnder300HoursTextarea()
  toggleOtherExperienceTextarea()

  $("input[name='experienceHoursOver300']").on("change", function() {
    toggleUnder300HoursTextarea();
  });

  // make sure that the hours and weeks boxes aren't displayed 
  // when they are hidden
  $("#yes300hours").on("click", function() {
    let hoursWeeksBoxes = $("#totalHours, #totalWeeks")
    $("#totalWeeks").val(8);
    $("#totalHours").val(300)
    hoursWeeksBoxes.prop('required', false); 
  })

  $("#no300hours").on("click", function() {
    let hoursWeeksBoxes = $("#totalHours, #totalWeeks")
    hoursWeeksBoxes.prop('required', true); 
  })

  $("#totalHours").on("input", function() {
    if ($(this).val() >= 300) {
      this.setCustomValidity('Please enter a number less than 300.')     
      this.reportValidity()        
    } else {
      this.setCustomValidity('')
    }
  })
    
  // Determine which checkbox was clicked and its current checked status, uncheck others
  let typeBoxes = $("#powerInequality, #communityIdentity, #civicLiteracy, #civicSkills")
  typeBoxes.on('click', function (event) {
    if (typeBoxes.filter(':checked').length > 0) {
      typeBoxes.prop('required', false);
    } else {
      typeBoxes.prop('required', true);
    } 
  });
  // ************** END SUMMER EXPERIENCE ************** //

  // ************** OTHER ENGAGEMENT ************** //
  $("input[name='experienceType']").on("change", function() {
    toggleOtherExperienceTextarea();
  });

  // ************** END OTHER ENGAGEMENT ************** //
})

function showEngagementInformation(engagementInfoDict) {
  let type = engagementInfoDict['type'],
      id = engagementInfoDict['id'],
      term= engagementInfoDict['term'];
  let username = $("#username").val()

  // based on how long the type is, get the remaining characters afterwards that represent the id
  $.ajax({
    url: `/cceMinor/${username}/getEngagementInformation/${type}/${term}/${id}`,
    type: "GET",
    data: "",
    success: function(response) {
      // create the list that will store the html
      // will be joined later to make a string
      var html = [] 
      html.push("<div>")
      if (type == "program") {
        let program = response["program"]
        let events = response["events"]
        let totalHours = response["totalHours"]

        html.push(`<h4>${program} History</h4>`)
        html.push(`Total volunteer hours: ${totalHours}`)
        html.push("<ul>")

        // add a list element to the html for each event in our list of events
        // link to the event view page as well
        for (let i = 0; i < events.length; i++) {
          html.push(`<li><a href="/event/${events[i]["id"]}/view" target="_blank">${events[i]["name"]}</a> - ${events[i]["hoursEarned"]} hrs</li>`)
        }

        html.push("</ul>")
      } else {
        let course = response["course"]
        let instructors = response["instructors"]

        // only show the course abbreviation and name if they exist, or only show the ones that exist
        if (course["courseAbbreviation"] && course["courseName"]) {
          html.push(`<h4>${course["courseAbbreviation"]}: ${course["courseName"]}</h4>`)
        } else if (course["courseAbbreviation"]) {
          html.push(`<h4>${course["courseAbbreviation"]}</h4>`)
        } else {
          html.push(`<h4>${course["courseName"]}</h4>`)
        }
        // add important fields to display
        html.push(`<p><b>Instructors:</b> ${instructors.join(", ")}</p>`)
        html.push(`<p><b>Section Designation:</b> ${course["sectionDesignation"] || "None"}</p>`)
        html.push(`<p><b>Course Credit:</b> ${course["courseCredit"]}</p>`)
        html.push(`<p><b>SLC Component:</b> ${Boolean(course["hasSlcComponent"]) ? "Yes" : "No"}</p>`)
      }
      html.push("</div>")
      // modify the displayed html by joining together the list we have been pushing to
      $(`#set${term}`).html(html.join(""))
    },
    error: function(request, status, error) {
      msgFlash("Error displaying information!", "danger")
    }
  });
}

function toggleEngagementCredit(isChecked, engagementData, checkbox){
    engagementData['username'] = $("#username").val();

    $.ajax({
          url: `/cceMinor/${engagementData['username']}/modifyCommunityEngagement`,
          type: isChecked ? "PUT" : "DELETE",
          data: engagementData,
          success: function(response) {
              if (response == ""){ 
                let header = isChecked ? 'Added' : 'Removed';
                msgToast("Success!", header + " engagement for " + engagementData['name'])
              } else {
                msgToast("Error saving changes!", response)
                $(checkbox).prop('checked', false);
              }
            },
          error: function(request, status, error) {
            console.log(error)
            msgFlash("Error saving changes!", "danger")
          }
    });
}

function toggleUnder300HoursTextarea() {
  var noRadio = $('#no300hours');
  var conditionalTextBox = $('#hoursBelow300Container');
  if (noRadio.is(':checked')) {
    conditionalTextBox.show();
  } else {
    conditionalTextBox.hide();
    if ($('#yes300hours').is(':checked')) {
      $('#totalHours').val(300);
    }
  }
}

function toggleOtherExperienceTextarea() {
  var otherRadio = $('#otherExperience');
  var conditionalTextBox = $('#otherExperienceDescription');
  if (otherRadio.is(':checked')) {
    conditionalTextBox.show()
  } else {
    conditionalTextBox.hide()
  }
}
