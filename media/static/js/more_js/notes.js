/*$(function() {
	/*changeColumnsHeight();

	CKEDITOR.replace('texteditor');	

	var accent = $('body').data('accent');
	var theme = $('body').data('theme');
	var uid = $('body').data('userId');

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
	/*var openedId = window.location.hash.substr(4);
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
				response.user_accent = accent;		
				response.csrf = getCookie('csrftoken');
				window.location.hash = 'id=' + id;
				var result = template.compile(response);
				$('#noteContent').html(result);
				openedId = id;
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
	});

	$('body').on('click', '#addToFavoriteForm', function(event) {
		event.preventDefault();
		$('#addToFavorite').attr('disabled', true);
		console.log("add to favorite submit");
		$.ajax({
			url: '/api/favorite/',
			type: 'POST',
			data: {
				csrfmiddlewaretoken: getCookie("csrftoken"),
				type: 1,
				note: openedId,
			}, 
			success: function(json) {
				console.log(json);
				console.log('success');
				console.log($(this));
				if (json.id != null) {
					$('#addToFavorite').html('<i class="flaticon-heart-broken"></i>Удалить из избранного');
				} else {
					$('#addToFavorite').html('<i class="flaticon-heart"></i>Добавить в избранное');
				}
				$('#addToFavorite').attr('disabled', false);
			},
			error: function(json) {
				console.log(json);
				console.log('error');
			}
		});
	});

	$('body').on('click', '.favorite-animation', function(event) {
		var heart_icon = '<i class="flaticon-heart-fill ' + accent + '-fg" id="heart_anim" style="position: absolute; font-size: 2em; opacity: 0.8; display: none; z-index: 5;"></i>'
		$('body').append(heart_icon);
		var heart_anim = $('#heart_anim');
		heart_anim.css('top', event.pageY - 6);
		heart_anim.css('left', event.pageX - 6);
		var favorite_button = $('#favorite').find('i');

		heart_anim.show().animate({'top': favorite_button.offset().top, 'left': favorite_button.offset().left, 'opacity': 0.3, 'font-size': '1em'}, 1500, function() {
			heart_anim.remove();
		});
	})	
})*/

$(function() {
	var noteCollection = null;
	var accent = $('body').data('accent');
	var theme = $('body').data('theme');
	var uid = $('body').data('userId');
	var noteDetails = null;

	moment.locale('ru');
	$.ajaxSetup({
		headers: {'X-CSRFToken': getCookie("csrftoken")}
	});

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

	var Router = Backbone.Router.extend({
		routes: {
			"note/:id": "getNote",
			"*actions": "defaultRouter"
		}
	});

	var router = new Router;

	var Note = Backbone.Model.extend({
		defaults: {
			id: null,
			title: 'No title',
			content: 'Empty',
			comments: null,
			pub_date: null,
			views: 0,
			login: null,						
		},
		urlRoot: '/api/notes/',
	});

	var NotesList = Backbone.Collection.extend({
		model: Note,
		url: '/api/notes/',
	});

	var AddNoteView = Backbone.View.extend({
		tagName: 'div',
		className: 'addNoteForm',
		events: {
			'click .notePush': 'addNote'
		},
		'addNote': function(event) {
			var current = new Note();
			var noteData = {
				title: $('#noteForm-Title').val(),
				content: $('#noteForm-Content').val()
			}
			current.save(noteData, {
				success: function (note) {
					updateNoteCollection();
				}
			});
		}
	});

	var NotesListItemView = Backbone.View.extend({
		tagName: 'div',
		className: 'list-navigation__item',
		attributes: {
			"data-note-id": null,
		},
		events: {
			'click': 'onClick'
		},
		initialize: function(opt) {
			_.bindAll(this, 'render');
			this.model.bind('change', this.render);
			this.render();
		},
		render: function() {			
			var _this = this;
			$(this.el).empty();

			var source = $('#NoteListItemTemplate').html();
			var template = Handlebars.compile(source);
			var context = { 
				id: this.model.get('id'),
				title: this.model.get('title'),
				pub_date: moment(this.model.get('pub_date'), 'YYYY-MM-DD HH:mm:ss').fromNow()
			};

			$(this.el).html(template(context));

			return this;
		},
		onClick: function(event) {
			//noteDetails = new NoteView({el: $('#noteContent'), model: this.model});
			
			router.navigate('note/' + this.model.get('id'), {trigger: true});
		}
	});

	var NotesListView = Backbone.View.extend({
		collection: null,
		el: '#notesListWidget',

		initialize: function(opt) {
			this.collection = opt.collection;
			_.bindAll(this, 'render');
		},

		render: function() {
			var element = $(this.el);
			element.html('');

			this.collection.forEach(function(item) {
				var itemView = new NotesListItemView({
					model: item,
					attributes: {
						"data-note-id": item.id,
					}
				});
				itemView.render();
				element.append(itemView.el);
			});

			return this;
		}
	});

	var NoteView = Backbone.View.extend({
		tagName: 'div',
		model: Note,
		initialize: function(opt) {
			this.render();
			var views = this.model.get('views') + 1;
			this.model.set('views', views);
			this.model.save(this.model.changedAttributes());
		},
		render: function() {
			var element = $(this.el);
			element.html('');
			var m = this.model;
			console.log(m);

			var source = $('#NoteDetailTemplate').html();
			var template = Handlebars.compile(source);
			var context = { 
				title: m.get('title'), 
				user: m.get('login'),
				views: m.get('views'),
				content: m.get('content'),
				user_accent: accent,
			};

			$(element).html(template(context));
			return this;
		}
	});

	updateNoteCollection();
	var addNoteView = new AddNoteView({	el: $('.addNoteForm') });	

	
	function updateNoteCollection() {
		this.async = true;
		noteCollection = new NotesList();
		noteCollection.fetch({
			success: function(data) {
		        var notesList = new NotesListView({	collection: data});
		        notesList.render();		        

				Backbone.history.start();
		    },
		    error: function(data) {
		        console.log(data);
		    }
		});
	}

	$('#refreshNoteList').click(function(event) {
		updateNoteCollection();
		$(this).addClass('animation pulse');
		setTimeout(function() {	$('#refreshNoteList').removeClass('animation pulse');}, 1000);
	});	

	router.on('route:defaultRouter', function(actions) {
		console.log('defaultRouter');
	});

	router.on('route:getNote', function(id) {
		console.log('navigate to note #' + id);
		console.log(noteCollection);
		noteDetails = new NoteView({el: $('#noteContent'), model: noteCollection.get(id)});
		$('[data-note-id]').removeClass('active animation vibro');
		$('[data-note-id=' + id + ']').addClass('active animation vibro');
	});

	$('#readMode').click(function() {
		$(this).toggleClass('button--color-' + accent);
		if (theme == 'light') {
			$(this).toggleClass('button--color-black');
		}
	});
});