$(document).ready(function () {
	$('#printVolunteerInfo').on('click', function () {
		var win = window.open();
		self.focus();
		win.document.open();
		win.document.write("<html><body>");
		win.document.write($('#volunteerInformationTable').html());
		win.document.write('</body></html>');
		win.document.close();
		win.print();
		win.close();
	})
	$(".displayCheckbox").on('change', function(){
		let checkboxId = this.id;
		if ($('#' + checkboxId).is(':checked')) {
			$("." + checkboxId).show()
		} 
		else {
			$("." + checkboxId).hide()
		}
		
	})

})
