// Insert code here to run when the DOM is ready
$(document).ready( function() {
	$("button").click(function() {
		var button_id = $(this).attr('data-item-id');
		var delete_uri = "delete-item/";
		delete_uri = delete_uri + (button_id);
		$.get(delete_uri);
		$(this).parent().remove();
	});
});
