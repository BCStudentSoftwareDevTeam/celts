$(document).ready(function () {
	$("#volunteerInformationTableToPrint").hide()
	$("#tableCardToggle").on('click', function () {
		$("#volunteerInformationCardToPrint").toggle()
		$("#volunteerInformationTableToPrint").toggle()

		
		if ($("#tableCardToggle").text() == "Card View") {
			$("#tableCardToggle").text("Table View")
		} else {
			$("#tableCardToggle").text("Card View")
		}
			
		console.log($("#tableCardToggleLabel").text())
		updateTable()
	})
	$('#printVolunteerInfo').on('click', function () {
		let contentToPrint;
		let tableContent = $("#volunteerInformationTableToPrint");
		let cardContent = $("#volunteerInformationCardToPrint");
		if ($('#tableCardToggle').text()=='Card View') {
			contentToPrint = tableContent;
		} else {
			contentToPrint = cardContent;
		}
		contentToPrint.siblings().addClass('d-print-none')
		contentToPrint.removeClass('d-print-none')
		contentToPrint.addClass('d-print-block')
		window.print();
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
				} else {
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
	function sortVolunteers() {
		let sortedTable = $("#volunteerInformationTableToPrint");
		let entriesTable = sortedTable.find(".volunteerInfoEntries");
	
		entriesTable.sort(function (a, b) {
			let textA = a.getElementsByClassName('nameSelect')[0].innerText
			let textB = b.getElementsByClassName('nameSelect')[0].innerText
			return textA.localeCompare(textB);
		});
	
		entriesTable.appendTo(sortedTable);

		let sortedCards = $("#volunteerInformationCardToPrint .sort-here");
		let entriesCards = sortedCards.find(".volunteerInfoEntries");
	
		entriesCards.sort(function (a, b) {
			let textA = a.getElementsByClassName('nameSelect')[0].innerText
			let textB = b.getElementsByClassName('nameSelect')[0].innerText
			return textA.localeCompare(textB);
		});
	
		entriesCards.appendTo(sortedCards);
	};
	getCheckBoxes()
	updateTable()
	sortVolunteers()
})
