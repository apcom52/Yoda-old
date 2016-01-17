$(function() {
	$('#show-sidebar').click(function() {
		if(window.innerWidth <= 480) {
			$('.sidebar').slideToggle();
		} else {
			$('.sidebar').toggle();
		}
	});

	$('#searchField').on("change keyup paste", function() {
		console.log("form");
		var query = $('#searchField').val();
		$('.listview .item').show();
		if (query.length >= 2) {
			setTimeout(function() {				
				$('.item > .item-content > .title:not(:contains("'+query+'"))').parent().parent().slideUp('slow');		
			}, 500);	
		}
		return false;
	});

	$('#showAllNotes').click(function() {
		$('.listview .item').show();
	});
	$('#showMyNotes').click(function() {
		$('.listview .item').hide();
		$('.listview .item[data-my-note="true"]').show();
	});








	var loading_block = "<div class='loading'></div>";
	$('[data-library-file-id]').removeClass('accent_color');

	var openedId = window.location.hash.substr(4);
	var libraryFileTemplate = $('#libraryFileTemplate').html();
	//Mustache.parse(libraryFileTemplate); 

	var LibraryFileTpl = "\
		<div class='grid'>\
			<div class='col col-12'><b>Описание: </b>{{description}}</div>\
			<div class='col col-2'><i class='fa fa-archive'></i>{{size}}</div>\
			<div class='col col-2'><i class='fa fa-eye'></i>{{views}}</div>\
			<div class='col col-2'><i class='fa fa-download'></i>{{downloads}}</div>\
			<div class='col col-6'><a href='{{file}}'><button class='button--color-olive button--icon button--fit'><i class='fa fa-cloud-download'></i>Скачать</button></a></div>\
		</div>\
	";

	$(document).on('click', '[data-library-file-id]', function() {
		loadFileById($(this).data('libraryFileId'));
	});

	$('.left-col').height($(window).height());
	$('html').height($(window).height());
	$('html').bind("DOMSubtreeModified", function(){
		$('.left-col').height($('html').height());
	});	

	sendAjax("GET", "/api/library/tags?count=8", {},
		function(data) {
			var tagsTpl = '{{#tags}}\
				<div class="tag tag--color-{{color}}">\
					<input type="checkbox" id="popularTag{{id}}">\
					<label for="popularTag{{id}}">{{title}}</label>\
				</div>\
			{{/tags}}';
			console.log(data);
			$('#popular_tags').html(Mustache.render(tagsTpl, { tags: data}));
		},
		function(data) {
			console.log(data);
		});


	$('#uploadLibraryFile').ajaxForm({
		success: function(data) {
			console.log("success");
			console.log(data);
			loadFiles();
		},
		error: function(data) {
			console.log("error");
			console.log(data);
		}
	});


	loadFiles();

	function loadFiles() {
		$('#files-list').html(loading_block);
		$.get('/api/library/file/', function(data) {
			var json = data;
			$.get('/media/tpl/library/library-files-list.html', function (template) {
				$('#files-list').html(Mustache.render(template, { files: json }));

				if (openedId) {
					loadFileById(openedId);
				}
			});
		});
		
	}

	function loadFileById(id) {
		$('.library-file-window').remove();
		$('[data-library-file-id]').removeClass('accent_color');
		var current = $('[data-library-file-id="' + id + '"]');
		current.addClass('accent_color');
		current.after('<div class="library-file-window">' + loading_block + '</div>');

		$.get('/api/library/file/?id=' + id, function(data) {
			var response = data;
			response.size = humanFileSize(response.size);

			$.get('/media/tpl/library/library-file.html', function(template) {
				$('.library-file-window').html(Mustache.render(template, response));
				window.location.hash = 'id=' + id;
			});
		});
	}

	/*$('.library-search-block').click(function() {
		$('#files-list').html(loading_block);
		$.get('/api/library/file/?q=электротех', function(data) {
			var json = data;
			$.get('/media/tpl/library/library-files-list.html', function (template) {
				$('#files-list').html(Mustache.render(template, { files: json }));

				if (openedId) {
					loadFileById(openedId);
				}
			});
		});
	})*/

	/*$('.library-search-block .fa').click(function () {
		if ($(this).hasClass('fa-search')) {
			console.log('show search');
			$('.library-card-header').hide();
			$('.library-search-block .fa').removeClass('fa-search').addClass('fa-times');
			$('.library-search').show();
		} else {
			console.log('hide search');
			$('.library-card-header').show();
			$('.library-search-block .fa').removeClass('fa-times').addClass('fa-search');
			$('.library-search').hide();
		}		
	});*/
});