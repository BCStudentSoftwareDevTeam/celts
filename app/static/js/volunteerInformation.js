$(document).ready(function () {
	$('#printVolunteerInfo').on('click', function () {
		var win = window.open();
		self.focus();
		win.document.open();
		win.document.write("<html><body>");
		win.document.write($('#volunteerInformationToPrint').html());
		win.document.write('</body></html>');
		win.document.close();
		win.print();
		win.close();
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
