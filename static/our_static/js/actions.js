$(function() {
	$('.ui.checkbox').checkbox();
	$('.ui.radio.checkbox').checkbox();
	$('.altrone-popup').popup();
	/* таскбар */
  	var toggleSidebar = false;
  	$('.overlay').click(function() {
  		$('.sidebar').animate({left:"-45%"}, 500);
  		$('.overlay').fadeOut(200);  			
  		toggleSidebar = false;  		  		
  	});

  	$('.menu-open').click(function(){
  		$('.sidebar').animate({left:"0"}, 500);
  		$('.overlay').fadeIn(200);
  		$('.sidebar').slideDown();  		
  		toggleSidebar = true;
  	});

  	$('#menu').click(function() {
  		$('.sidebar').slideToggle();
  	});

    $('#up').click(function() {
        $("body, html").animate({scrollTop: 0}, 800);
        //window.scroll(0, 0);
        $('#up').fadeOut('fast');
    });


    //Подтверждение событий
    function sendEventAnswer(url, method, data, on_success, on_error) {
        console.log('sending post...');
        $.ajax({
            url: url,
            type: method, 
            data: data,
            success: on_success(data),
            failure: on_error(data),
        }); 
    }

    /*$('#event-visit-yes').click(function(){
        console.log('yes');
        sendEventAnswer('/events/answer/', 'post', {event_id: $(this).data('eventId'), answer: 1}, function(data) {
            alert('Success!');
        }, function(data) { alert('Error'); });
    });
    $('#event-visit-maybe').click(function(){
        console.log('maybe');
        sendEventAnswer($(this).data('eventId'), 2);
    });
    $('#event-visit-no').click(function(){
        console.log('no');
        sendEventAnswer($(this).data('eventId'), 3);
    });*/
})