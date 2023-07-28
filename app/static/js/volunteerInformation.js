$(document).ready(function () {
	$("#volunteerInformationTableToPrint").hide()
	$("#tableCardToggle").on('change', function () {
		$("#volunteerInformationCardToPrint").toggle()
		$("#volunteerInformationTableToPrint").toggle()

		
		if ($("#tableCardToggleLabel").text() == "Card View") {
			$("#tableCardToggleLabel").text("Table View")
		} else {
			$("#tableCardToggleLabel").text("Card View")
		}
			
		console.log($("#tableCardToggleLabel").text())
		updateTable()
	})
	$('#printVolunteerInfo').on('click', function () {
		let contentToPrint, contentToHide
		if ($('#tableCardToggle').is(':checked')) {
			contentToPrint = $("#volunteerInformationTableToPrint")
			contentToHide = $("#volunteerInformationCardToPrint")
		} else {
			contentToPrint = $("#volunteerInformationCardToPrint")
			contentToHide = $("#volunteerInformationTableToPrint")
		}
		contentToPrint.siblings().hide()
		contentToPrint.parents().siblings().hide()
		if (contentToPrint.length > 1) {
			contentToPrint.css('column-count', '2');	
		} 
		window.print()
		contentToPrint.siblings().show()
		contentToPrint.parents().siblings().show()
		contentToPrint.css('column-count', '1');
		contentToHide.hide()
		
		
	})
	$(".displayCheckbox").on('change', function () {
		getCheckBoxes()
		updateTable()
	})
	function updateTable() {
		let allEntries = $(".volunteerInfoEntries")
		let shownUsers = []
		for (let i = 0; i < allEntries.length; i++) {
			let currentEntry = $(allEntries[i])
			if (!currentEntry.is(":hidden")) {
				if (shownUsers.includes(currentEntry.data("user"))) {
					currentEntry.hide()
				}
				else {
					shownUsers.push(currentEntry.data("user"))
				}

			}
		}
	}
	
	function getCheckBoxes() {
		$(".displayCheckbox").each(function () {
			let checkboxId = this.id;
			if ($('#' + checkboxId).is(':checked')) {
				$("." + checkboxId).show()
			}
			else {
				$("." + checkboxId).hide()
			}
		})
	}
	getCheckBoxes()
	updateTable()
})
