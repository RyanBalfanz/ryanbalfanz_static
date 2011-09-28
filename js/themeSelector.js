$('#theme-primary').click(function() {
	$(".chart rect").css('fill', 'steelblue');
	$("li#theme-primary").addClass('active');
	$("li#theme-secondary").removeClass('active');
});

$('#theme-secondary').click(function() {
	$(".chart rect").css('fill', 'darkorange');
	$('li#theme-primary').removeClass('active');
	$('li#theme-secondary').addClass('active');
});