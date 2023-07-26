$(document).ready(function() {
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