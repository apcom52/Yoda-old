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

	var Settings = Backbone.Model.extend({
		defaults: {
			id: null,
			username: null,
			avatar: null,
			facebook: null,
			twitter: null,
			vk: null,
			github: null,
			phone: null,
			theme: null,
			accent: null,
			beta: null,
			hide_email: null,
			hide_tips: null,
			filter_achievements: null,
			filter_sales: null,
			filter_catapult: null,
			filter_bonuses: null,
			notes_night_mode: null,
			notes_font_size: null,
			notes_font_style: null,
			polls_actual: null,
			events_notification: null,
			events_time_notification: null
		}, 
		urlRoot: "/api/settings/",
		url: function() {
			var url = this.urlRoot + '?';
			return url;
		}
	});

	var settings = new Settings();
	settings.fetch();
	
	
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
		$('.y-sidebar').removeClass('invert');
		$('body').css('background-color', 'lightblue');
		$('.y-friends-list').removeClass('invert');
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
		$('.y-sidebar').addClass('invert');
		$('body').css('background-color', 'gray');
		$('.y-friends-list').addClass('invert');

		/*settings.save({theme: 'dark'}, {
			success: function(d) { console.log('success'); console.log(d); },
			error: function(e) { console.log('err'); console.log(e); }
		});*/
	});

	function resetAllAccents() {
		resetAccent('.list', 'list--color');
		resetAccent('#mainMenu', 'taskbar__item--hover-color')
		resetAccent('.select', 'select--color');
		resetAccent('.checkbox', 'checkbox--color');
		resetAccent('.toggle', 'toggle--color');
		resetAccent('.accentButton', 'button--color');
		resetAccent('.y-sidebar-list', 'y-sidebar-list--color');

		var array = ['red', 'orange', 'yellow', 'olive', 'green', 'blue', 'teal', 'purple', 'violet', 'pink', 'brown'];
		for (var i = 0; i < array.length; i++) {
			$('a').removeClass(array[i]+'-fg');	
			$('.y-sidebar > .cover').removeClass(array[i]+'-bg');		
			$('#back_menu').removeClass(array[i]+'-bg');
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
		$('.y-sidebar-list').addClass('y-sidebar-list--color-' + color);
		$('a').addClass(color + '-fg');
		$('.y-sidebar > .cover').addClass(color + '-bg');
		$('#back_menu').addClass(color + '-bg');
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
	});

	$('#settingsLogo').click(function() {
		var _this = $(this);
		_this.addClass('animation fanfare');
		setTimeout(function() {
			_this.removeClass('animation fanfare');
			console.log('timeout');
		}, 1500);
	});
});