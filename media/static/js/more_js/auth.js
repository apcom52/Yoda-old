$(function() {	
	$('html').height($(window).height());

	$('#currentUser').click(function() {		
		$('.users-list').slideDown(500);
	});

	$('#closeUsersList').click(function() {
		$('.users-list').slideUp(500);
		$('.switch-user-btn').removeAttr("style");
	});	

	$('.users-list__item').click(function() {
		$('.users-list__item').removeClass('users-list__item--active');
		$(this).addClass('users-list__item--active');

		var photo_url = $(this).find('img').attr('src');
		var first_name = $(this).find('span').html();
		var user_name = $(this).find('span').data('username');

		$('#userProfilePhoto').attr('src', photo_url);
		$('#currentUserName').html(first_name);

		$('.users-list').slideUp(500);
		$('.switch-user-btn').removeAttr("style");

		$('#userName').val(user_name);
	});

	$('#signInBtn').click(function() {
		if (($('#userPassword').val()).length > 5) {
			//console.log($('#signInForm').serialize());
			$('#signInForm').submit();
			$('.alert').hide();
		} else {
			$('.alert').hide();
			$('#currentUser').after('<div class="alert alert--red-bg margin-top-1"><div class="alert__content">Пароль должен быть не менее 6 символов</div></div>');
		}
	})
});