$(document).ready(function () {
	var userdata = $('.volunteerInfoEntries');
	var users = userdata.map((index,row) => {
		return $(row).data('user');
    }).get();
	users = new Set(users);
	users = [... users]
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
	$(".displayCheckbox").on('change', function () {
		getCheckBoxes()
	})
	$.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
		if (settings.nTable.id !== 'volunteerInformationTableToPrint') {
			return true;
		}

		const status = data[3].toLowerCase(); // Volunteer Status column

		if (status === 'attended' && !$('#attendedSelect').is(':checked')) return false;
		if (status === 'rsvp' && !$('#rsvpSelect').is(':checked')) return false;
		if (status === 'waitlist' && !$('#waitlistSelect').is(':checked')) return false;

		return true;
	});
	function hideDuplicateVolunteers() {
		let allEntries = $("#volunteerInformationCardToPrint .volunteerInfoEntries");
		let shownUsers = [];
		allEntries.each(function () {
        let currentEntry = $(this);
        let user = currentEntry.data("user");
			if (currentEntry.is(":visible")) {
				if (shownUsers.includes(user)) {
					currentEntry.hide()
				} else {
					shownUsers.push(user);
				}
			}
		});
	}
	function getCheckBoxes() {
		$(".displayCheckbox").each(function () {
			let checkboxId = this.id;
			if ($('#' + checkboxId).is(':checked')) {
				$("#volunteerInformationCardToPrint ." + checkboxId).show();
			} else {
				$("#volunteerInformationCardToPrint ." + checkboxId).hide();
			}
			});
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

	var volunteerInfoTable= $('#volunteerInformationTableToPrint').DataTable({ stripeClasses: []});
	getCheckBoxes()
	hideDuplicateVolunteers()
	sortVolunteers()
	for(let i = 0; i < users.length; i++){
		$('#volunteerUsernames').append(`<input type="hidden" name="username" value=${users[i]}>`)
	}
$("#travelFormItem").on("click", function(){
			$("#volunteerUsernames").submit()
})
$("#volutneerListItem").on("click", function(){
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

});