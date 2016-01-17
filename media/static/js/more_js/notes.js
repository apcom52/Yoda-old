$(function() {
	changeColumnsHeight();

	$(window).resize(function() {
		changeColumnsHeight();
	})

	function changeColumnsHeight() {
		var lc = $('#leftCol').height();
		var rc = $('#rightCol').height();

		var note_content = $('#noteContent').height();

		if (lc >= note_content) {
			$('#rightCol').height(lc);
		} else {
			$('#leftCol').height(note_content);			
		}

		$('#rightCol').height(note_content);
	}

	$('body').on('click', '#expandNoteOptions', function() {
		console.log('cl');
		if ($('#noteOptions').is(':visible')) {
			$('#noteOptions').slideUp(500, function() {
				changeNoteHeight();
			});
			$('#expandNoteOptions').find('i').removeClass('flaticon-up').addClass('flaticon-down');
			
		} else {
			$('#noteOptions').slideDown(500, function() {
				changeNoteHeight();
			});
			$('#expandNoteOptions').find('i').removeClass('flaticon-down').addClass('flaticon-up');
		}
	})

	$(document).on("touchstart", function(event) {
		$(window).swipe({
		  	swipeRight:function(event, direction, distance, duration, fingerCount) {
		  		if ($('#leftCol').css('position') == 'absolute') {
		  			console.log('swipeRight');
		    		$('#leftCol').animate({left: '0px'}, 1000);
		    	}
		  	}, 
		  	swipeLeft:function(event, direction, distance, duration, fingerCount) {
		  		if ($('#leftCol').css('position') == 'absolute') {
			  		console.log('swipeLeft');
			    	$('#leftCol').animate({left: '-600px'}, 1000);
			    }
		  	}
		});
	});

	/* Открытие заметки */
	/* Если при загрузке страницы в URL уже есть индекс заметки, то переходим по нему */
	var openedId = window.location.hash.substr(4);
	var loading_block = "<div class='loading'></div>";
	if (openedId) {
		showNote(openedId);
		$('[data-note-id="'+ openedId +'"]').addClass('active');
	}

	
	$('[data-note-id]').on('click', function() {
		var note_id = $(this).data('noteId');
		$('.list-navigation__item').removeClass('active');
		$(this).addClass('active');
		showNote(note_id);	

		if ($('#leftCol').css('position') == 'absolute') {
	    	$('#leftCol').animate({left: '-600px'}, 1000);
	    }	
	});

	function showNote(id) {
		$('#noteContent').html(loading_block);		

		$.get('/media/tpl/notes/note.html', function(tpl) {
			var template = Walrus.Parser.parse(tpl);

			$.get('/api/notes?id=' + id, function(response) {				
				window.location.hash = 'id=' + id;
				var result = template.compile(response);
				$('#noteContent').html(result);
				changeNoteHeight();
				changeColumnsHeight();
			});
		});
	}

	function changeNoteHeight() {
		var result_height = $('#note_title').outerHeight() + $('#note_actions').outerHeight()+ $('#note_text').outerHeight();				
		$('#rightCol').css('height', result_height + 'px');
	}

	$('body').append('<div class="overlay"></div>');
	$('#search').click(function() {	
		if ($('.search_block').is(':visible')) {
			$('.search_block').slideUp(500);
			$('.overlay').animate({'opacity': 0}, 500, function() { $('.overlay').hide(); });
		} else {
			$('.search_block').slideDown(500);
			$('.overlay').show().css('opacity', 0).animate({'opacity': 1}, 500);
			$('#search_field').focus();
		}
	});

	$('body').on('click', '.overlay', function() {
		$('.search_block').slideUp(500);
		$('.overlay').animate({'opacity': 0}, 500, function() { $('.overlay').hide(); });
	});

	$('#search_field_help').click(function() {
		$('#search_field').attr('value', $('#search_field_help').html()).focus();
	})
})