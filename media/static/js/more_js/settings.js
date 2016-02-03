$(function() {
	$.ajaxSetup({
		headers: {'X-CSRFToken': getCookie("csrftoken")}
	});

	var Router = Backbone.Router.extend({
		routes: {
			"*card_id": "default"
		}
	});

	var router = new Router;	

	router.on('route:default', function(card_id) {
		console.log(card_id);
		$('.settings-card').hide();
		$('#' + card_id).show();
		$('.list__item').removeClass('list__item--active');
		$('.list__item[data-settings-target="' + card_id + '"]').addClass('list__item--active');
	});

	Backbone.history.start();
	
	$('#font14').click(function() { $('#notesPreviewText').css('font-size', '14px'); });
	$('#font16').click(function() { $('#notesPreviewText').css('font-size', '16px'); });
	$('#font18').click(function() { $('#notesPreviewText').css('font-size', '18px'); });
	$('#font20').click(function() { $('#notesPreviewText').css('font-size', '20px'); });

	$('#fontScreen').click(function() { $('#notesPreviewText').css('font-family', 'PT Sans'); });
	$('#fontBook').click(function() { $('#notesPreviewText').css('font-family', 'serif'); });

	$('#notesDarkTheme').click(function() {
		if ($(this).prop('checked')) {
			$('#notesPreviewText').addClass('alert--black-bg');
		} else {
			$('#notesPreviewText').removeClass('alert--black-bg');
		}
	});

	$('#lightTheme').click(function() {
		$('.taskbar').removeClass('taskbar--invert');
		$('.dropdown').removeClass('dropdown--invert');
		$('.card').removeClass('card--colored card--color-black');
		$('.select').removeClass('select--invert');
		$('.list').removeClass('list--invert');
		$('.checkbox').removeClass('checkbox--invert');
		$('.toggle').removeClass('toggle--invert');
		$('.form').removeClass('form--invert');
		$('body').css('background-color', 'lightblue');

		$.get('/api/settings/?m=theme&theme=light', function() {
			console.log('Тема изменена на светлую');
		});
	});

	$('#darkTheme').click(function() {
		$('.taskbar').addClass('taskbar--invert');
		$('.dropdown').addClass('dropdown--invert');
		$('.card').addClass('card--colored card--color-black');
		$('.select').addClass('select--invert');
		$('.list').addClass('list--invert');
		$('.checkbox').addClass('checkbox--invert');
		$('.toggle').addClass('toggle--invert');
		$('.form').addClass('form--invert');
		$('body').css('background-color', 'gray');

		$.post('/api/settings/', {
			'm': 'theme',
			'theme': 'dark',
		}, function(d) {
			console.log(d);
			console.log('Тема изменена на темную');
		});
	});

	function resetAllAccents() {
		resetAccent('.list', 'list--color');
		resetAccent('#mainMenu', 'taskbar__item--hover-color')
		resetAccent('.select', 'select--color');
		resetAccent('.checkbox', 'checkbox--color');
		resetAccent('.toggle', 'toggle--color');
		resetAccent('.accentButton', 'button--color');

		var array = ['red', 'orange', 'yellow', 'olive', 'green', 'blue', 'teal', 'purple', 'violet', 'pink', 'brown'];
		for (var i = 0; i < array.length; i++) {
			$('a').removeClass(array[i]+'-fg');			
		};
	}

	function resetAccent(element, mask) {
		var array = ['red', 'orange', 'yellow', 'olive', 'green', 'blue', 'teal', 'purple', 'violet', 'pink', 'brown'];
		for (var i = 0; i < array.length; i++) {
			$(element).removeClass(mask + '-' + array[i]);			
		};
	}

	function setAccent(color) {
		resetAllAccents();

		$('.list').addClass('list--color-' + color);
		$('#mainMenu').addClass('taskbar__item--hover-color-' + color);
		$('.select').addClass('select--color-' + color);
		$('.checkbox').addClass('checkbox--color-' + color);
		$('.toggle').addClass('toggle--color-' + color);
		$('.accentButton').addClass('button--color-' + color);
		$('a').addClass(color + '-fg');
	}

	$('#accentRed').click(function() { setAccent('red'); });
	$('#accentOrange').click(function() { setAccent('orange'); });
	$('#accentYellow').click(function() { setAccent('yellow'); });
	$('#accentOlive').click(function() { setAccent('olive'); });
	$('#accentGreen').click(function() { setAccent('green'); });
	$('#accentBlue').click(function() { setAccent('blue'); });
	$('#accentTeal').click(function() { setAccent('teal'); });
	$('#accentPurple').click(function() { setAccent('purple'); });
	$('#accentViolet').click(function() { setAccent('violet'); });
	$('#accentPink').click(function() { setAccent('pink'); });
	$('#accentBrown').click(function() { setAccent('brown'); });

	$('.color-block').click(function() {
		$('.color-block').removeClass('active');
		$(this).addClass('active');
	})
});