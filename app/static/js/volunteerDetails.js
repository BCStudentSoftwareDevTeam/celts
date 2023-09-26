$(document).ready(function () {
	$("#tableCardToggle").on('click', function () {
		$("#volunteerInformationCardToPrint").toggle()
		$("#volunteerInformationTableToPrint_wrapper").toggle()

		if ($("#tableCardToggle").text() == "Card View") {
			$("#tableCardToggle").text("Table View")
			$(".bNumberSelect").toggle()
		} else {
			$("#tableCardToggle").text("Card View")
			$(".bNumberSelect").toggle()
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
	})
	function hideDuplicateVolunteers() {
		let allEntries = $(".volunteerInfoEntries")
		let shownUsers = []
		for (let i = 0; i < allEntries.length; i++) {
			let currentEntry = $(allEntries[i])
			if (currentEntry.is(":visible")) {
				if (shownUsers.includes(currentEntry.data("user"))) {
					currentEntry.hide()
				} else {
					shownUsers.push(currentEntry.data("user"))
				}
			}
		}
		stripeVolunteerInfoTable()
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
		hideDuplicateVolunteers()

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

	function stripeVolunteerInfoTable() {
		$('#volunteerInformationTableToPrint .volunteerInfoEntries').removeClass('custom-odd custom-even')
		$('#volunteerInformationTableToPrint .volunteerInfoEntries:visible').each(function (i,e) {
			$(e).addClass(i % 2 ? 'custom-odd' : 'custom-even')
		})
	}

	getCheckBoxes()
	hideDuplicateVolunteers()
	sortVolunteers()
	var volunteerInfoTable= $('#volunteerInformationTableToPrint').DataTable({ stripeClasses: []});
	volunteerInfoTable.on('draw.dt', function (){
		getCheckBoxes()
		stripeVolunteerInfoTable()
	});
	stripeVolunteerInfoTable()
});
