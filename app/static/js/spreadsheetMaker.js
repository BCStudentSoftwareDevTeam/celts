$(document).ready(function(){
	$("#createSpreadsheet").on("click", function(){

		$.ajax({
			method: "POST",
			url: "/createSpreadsheet/",
			data: {"academicYear": $("#academicYear").val(),
				   "academicTerm": $("#academicTerm").val()},
			success: function(response) {
				console.log(data)
			}
			
		  });
	})
})