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
		let tableContent = $("#volunteerInformationTableToPrint")
		let cardContent = $("#volunteerInformationCardToPrint")
		if ($('#tableCardToggle').is(':checked')) {
			contentToPrint = tableContent
			contentToHide = cardContent
		} else {
			contentToPrint = cardContent
			contentToHide = tableContent
		}
		contentToPrint.siblings().hide()
		contentToPrint.parents().siblings().hide()
		// // let checkContentLength = $("#"+cardContent[0].id+" .volunteerInfoEntries").length
		// // console.log((contentToPrint == cardContent) && (checkContentLength > 1))
		// if (contentToPrint == cardContent) {
		contentToPrint.css('column-count', '2');
		contentToPrint.css("break-inside", "avoid");
		// } 
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
	$("#sortFirstName").on('click', function() {
		let $sortedTable = $("#volunteerInformationTableToPrint");
		let $entriesTable = $sortedTable.find(".volunteerInfoEntries");
	
		$entriesTable.sort(function (a, b) {
			return a.dataset.fullname.localeCompare(b.dataset.fullname);
		});
	
		$entriesTable.appendTo($sortedTable);

		let $sortedCards = $("#volunteerInformationCardToPrint .sort-here");
		let $entriesCards = $sortedCards.find(".volunteerInfoEntries");
	
		$entriesCards.sort(function (a, b) {
			return a.dataset.fullname.localeCompare(b.dataset.fullname);
		});
	
		$entriesCards.appendTo($sortedCards);
	});
	$("#sortUsername").on("click", function() {
		let $sortedTable = $("#volunteerInformationTableToPrint");
		let $entriesTable = $sortedTable.find(".volunteerInfoEntries");
	
		$entriesTable.sort(function (a, b) {
			return a.dataset.user.localeCompare(b.dataset.user);
		});
	
		$entriesTable.appendTo($sortedTable);

		let $sortedCards = $("#volunteerInformationCardToPrint .sort-here");
		let $entriesCards = $sortedCards.find(".volunteerInfoEntries");
	
		$entriesCards.sort(function (a, b) {
			return a.dataset.user.localeCompare(b.dataset.user);
		});
	
		$entriesCards.appendTo($sortedCards);
	})
	getCheckBoxes()
	updateTable()
})
