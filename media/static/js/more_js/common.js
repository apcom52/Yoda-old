$(function() {
	var accent = $('body').data('accent');

	$.ajaxSetup({
		headers: {'X-CSRFToken': getCookie("csrftoken")}
	});

	$(window).scroll(function () {
		if ($(this).scrollTop() >= 44) {
			$('.y-sidebar').css('top', '0px');
			$('.y-friends-list').css('top', '0px');
			console.log('more 44');
		} else {
			$('.y-sidebar').css('top', (44 - $(window).scrollTop()) + 'px');
			$('.y-friends-list').css('top', (44 - $(window).scrollTop()) + 'px');
			console.log('less 44');
		}
	});

	var sidebar_visible = false;
	$('#mainMenu').click(function() {
		showSidebar();
	});

	$('#back_menu').click(function() {
		hideSidebar();
	});

	function showSidebar() {
		if (sidebar_visible == false) {
			$('.y-sidebar').animate({left: '0px'}, 1000);
			$('.user-avatar').addClass('visible');

			sidebar_visible = true;
			$('#mainMenu').hide();
			$('#back_menu').show();
		}
	}

	function hideSidebar() {
		if (sidebar_visible == true) {
			$('.y-sidebar').animate({left: '-450px'}, 750);
			$('.user-avatar').removeClass('visible');

			sidebar_visible = false;
			$('#back_menu').hide();
			$('#mainMenu').show();
		}
	}

	var Friend = Backbone.Model.extend({
		defaults: {
			id: 0,
			first_name: "",
			last_name: "",
			avatar: "",
			is_online: false,
		},
		urlRoot: "/api/users/",
		url: function() {
			var url = this.urlRoot + '?' + this.id;
			return url;
		}
	});

	var FriendList = Backbone.Collection.extend({
		model: Friend,
		url: '/api/users/',
	});

	var FriendListView = Backbone.View.extend({
		collection: null,
		el: '#friendsContent',

		initialize: function(opt) {
			this.collection = opt.collection;
			_.bindAll(this, 'render');
		},

		render: function() {
			var element = $(this.el);
			element.html('');

			this.collection.forEach(function(item) {
				var itemView = new FriendListItemView({
					model: item,
					attributes: {
						'data-friends-id': item.id
					}
				});
				itemView.render();
				element.append(itemView.el);
			});

			return this;
		}
	});

	var FriendListItemView = Backbone.View.extend({
		tagName: 'div',
		className: 'y-friends-list__item',
		attributes: {
			'data-user-id': null,
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

			var source = $('#friendListItemTemplate').html();
			var template = Handlebars.compile(source);
			var context = { 
				id: this.model.get('id'),
				username: this.model.get('first_name') + ' ' + this.model.get('last_name'),
				avatar: this.model.get('avatar'),
				accent: accent,
				online: this.model.get('is_online'),
			};
			$(this.el).html(template(context));

			return this;
		}
	});

	function updateFriendList() {
		var friendsCollection = new FriendList();
		friendsCollection.fetch({
			success: function(data) {
				var friendsList = new FriendListView({ collection: data});
				friendsList.render();
				console.log(friendsCollection);
			},
			error: function(data) {
				console.log('error');
			}
		});
	}

	var friends_visible = false;
	$('#showFriends').click(function() {
		if (!friends_visible) {
			$('.y-friends-list').animate({right: '0px'}, 500);
			updateFriendList();
			$('#showFriends').addClass(accent + '-bg');
			$('#showFriends').addClass('white-fg');
			friends_visible = true;
		} else {
			$('.y-friends-list').animate({right: '-300px'}, 300);
			$('#showFriends').removeClass(accent + '-bg');
			$('#showFriends').removeClass('white-fg');
			friends_visible = false;
		}
	});	
});