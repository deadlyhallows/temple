jQuery(document).ready(function() {
	$('.launch-modal').on('click', function(e){
		e.preventDefault();
		console.log("gh1");
		$('#' + $(this).data('modal-id')).modal({backdrop: 'static'});
		console.log('#' + $(this).data('modal-id'));
		
	});

});




