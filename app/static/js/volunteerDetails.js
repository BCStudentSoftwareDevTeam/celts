$(document).ready(function () {
	
	$("#volunteerInformationCardToPrint").toggle()
	$("#tableCardToggle").on('click', function () {
		$("#volunteerInformationCardToPrint").toggle()
		$("#volunteerInformationTableToPrint_wrapper").toggle()

		if ($("#tableCardToggle").text() == "Card View") {
			$("#tableCardToggle").text("Table View")
		} else {
			$("#tableCardToggle").text("Card View")
		}
		hideDuplicateVolunteers()
	})
	$('#printVolunteerInfo').on('click', function () {
		let contentToPrint;
		let tableContent = $("#volunteerInformationTableToPrint_wrapper");
		let cardContent = $("#volunteerInformationCardToPrint");
		if ($('#tableCardToggle').text() == 'Card View') {
			contentToPrint = tableContent;
		} else {
			contentToPrint = cardContent;
		}
		contentToPrint.siblings().addClass('d-print-none');
		contentToPrint.removeClass('d-print-none');
		$(".always-print").removeClass('d-print-none');
		let getTableLength = volunteerInfoTable.page.len();
		let getTablePage = volunteerInfoTable.page();
		volunteerInfoTable.page.len(-1).draw();
		window.print();
		volunteerInfoTable.page.len(getTableLength).draw();
		volunteerInfoTable.page(getTablePage).draw('page');
	})
	$(".displayCheckbox").on('change', function () {
		getCheckBoxes()
		hideDuplicateVolunteers()
	})
	function hideDuplicateVolunteers() {
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
		let sortedTable = $("#volunteerInformationTableToPrint_wrapper");
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
	hideDuplicateVolunteers()
	sortVolunteers()
	var volunteerInfoTable= $('#volunteerInformationTableToPrint').DataTable({ "ordering": true });
	volunteerInfoTable.on('draw.dt', function (){
		getCheckBoxes()
	});
});