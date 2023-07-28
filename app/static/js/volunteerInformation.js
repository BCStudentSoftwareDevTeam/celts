$(document).ready(function () {
	$('#printVolunteerInfo').on('click', function () {
		$('#volunteerInformationToPrint').siblings().hide()
		$('#volunteerInformationToPrint').parents().siblings().hide()
		$('#volunteerInformationToPrint').css('column-count', '2');
		window.print()
		$('#volunteerInformationToPrint').siblings().show()
		$('#volunteerInformationToPrint').parents().siblings().show()
		$('#volunteerInformationToPrint').css('column-count', '1');
		
		
	})
	$(".displayCheckbox").on('change', function(){
		$(".displayCheckbox").each(function() {
			let checkboxId = this.id;
			if ($('#' + checkboxId).is(':checked')) {
				$("." + checkboxId).show()
			} 
			else {
				$("." + checkboxId).hide()
			}
		})
		updateTable()
	})
	function updateTable() {
		let allEntries = $("#volunteerInformationToPrint .volunteerInfoEntries")
		let shownUsers = [] 
		for (let i=0; i < allEntries.length; i++) {
			let currentEntry = $(allEntries[i])
			if (!currentEntry.is(":hidden")) {
				if (shownUsers.includes(currentEntry.data("user"))) {
					currentEntry.hide()
				}
				else {
					shownUsers.push(currentEntry.data("user"))
				}
				console.log(shownUsers)
			}
		}
	}
	updateTable()
})
