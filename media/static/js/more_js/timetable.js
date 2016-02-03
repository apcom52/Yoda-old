$(function() {
	$('[data-lesson-title]').click(function() {
		$('.timetable-day__list__item').css({opacity: 0.1});
		var lesson_title = $(this).data('lessonTitle');
		$('.timetable-day__list__item[data-lesson-title="'+ lesson_title +'"]').css({opacity: 1});
	});

	$(document).click(function(e) {
		if ($(e.target).closest('[data-lesson-title]').length)
			return;
		$('.timetable-day__list__item').css({opacity: 1});
		e.stopPropagation();
	});
});