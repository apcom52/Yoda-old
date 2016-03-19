$(function() {

    /*Modernizr.load({
        test: Modernizr.geolocation,
        yep : 'geo.js',
        nope: 'geo-polyfill.js'
    });*/

    /*$.ajax({
        type: "POST",
        url: "/api/library/tag-category",
        data: {
            "csrfmiddlewaretoken": "ve7TrvFXQYLNlnHlZScE3zTetIyAkTy8",
            "title": "из ajax",
            "color": "yellow",
        },
        success: function(data) {
            console.log(data);
        }
    });*/

	$('.ui.checkbox').checkbox();
	$('.ui.radio.checkbox').checkbox();
	$('.altrone-popup').popup();
    $('.special.cards .image').dimmer({on: 'hover'});

	/* таскбар */
  	var toggleSidebar = false;
  	$('.overlay').click(function() {
  		$('.sidebar').animate({left:"-45%"}, 500);
        $('.notification-center').animate({right:"-45%"}, 500);
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

    $('#notification_center_opened').click(function(){
        $('.notification-center').animate({right:"0"}, 500);
        $('.overlay').fadeIn(200);   
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

    /* Скроллинг и кнопка "Вверх" */
    $('.altrone-up').hide()
    $(window).scroll(function() {
        if ($(this).scrollTop() > 200) $('.altrone-up').slideDown();
        else $('.altrone-up').slideUp();
    })
    $('.altrone-up').click(function() {
        $('body, html').animate({
            scrollTop: 0
        }, 1000);
    })

    /* Вставка смайликов в текст */
    $('.altrone-smile').click(function() {
        $('#comment').append(':|' + $(this).data('smileCode') + '|:');
    });

    /* Рулетка */
    var itemid = $('.rulette').data('presentId');
    var timerId = setInterval(function() {
        $('.rulette .row .item').removeClass('blink', 250);
        var rnd = Math.round(1 + Math.random() * (15));
        $('#ruletteItem' + rnd).addClass('blink', 250);
    }, 250);

    setTimeout(function() {
        clearInterval(timerId);
        $('.rulette .row .item').removeClass('blink', 'fast');
        $('#ruletteItem' + itemid).addClass('selected');
        
    }, 4000);

    setTimeout(function() {
        $('.rulette').slideUp(1000);
        $('.rulette-message').show();
    }, 6000);




    /* Рулетка случайный бонус */
    var bingoItemId = $('.bingo-rulette').data('presentId');
    var bingoTimerId = setInterval(function() {
        $('.bingo-rulette .row .item').removeClass('blink', 250);
        var rnd = Math.round(1 + Math.random() * (11));
        $('#bingoItem' + rnd).addClass('blink', 250);
    }, 250);

    setTimeout(function() {
        clearInterval(bingoTimerId);
        $('.bingo-rulette .row .item').removeClass('blink', 'fast');
        $('#bingoItem' + bingoItemId).addClass('selected');
        
    }, 4000);

    setTimeout(function() {
        $('.bingo-rulette').slideUp(1000);
        $('.bingo-rulette-message').show();
    }, 6000);


    /* Рулетка лотерея */
    var bingoItemId = $('.lottery-items').data('presentId');
    var bingoTimerId = setInterval(function() {
        $('.lottery-items .row .item').removeClass('blink', 250);
        var rnd = Math.round(1 + Math.random() * (11));
        $('#lotteryItem' + rnd).addClass('blink', 250);
    }, 250);

    setTimeout(function() {
        clearInterval(bingoTimerId);
        $('.lottery-items .row .item').removeClass('blink', 'fast');
        $('#lotteryItem' + bingoItemId).addClass('selected');        
    }, 6500);

    setTimeout(function() {
        console.log('swipe');
        $('.lottery-items').slideUp(1000);
        $('.lottery-message').show();
        var audio = $("#lottery-sound")[0];
        //audio.play();
    }, 8000);


    // Передача предмета другу
    $('.send-item-to-friend').click(function() {
        $('.send-item-modal').modal('show');
    });

    $('.send-catapult').click(function() {
        $('.catapult-success-message').hide();
        $('.catapult-error-message').hide();
        $('.send-catapult').prop('disabled', false);
        var value = $('#catapult-items').val();
        $.ajax({
            type: "POST",
            url: "/users/send_catapult/",
            data: {
                'item_id': value,
            },
            success: function(data) {
                if (data != 'no') {
                    $('.catapult-success-message').html('Ваш подарок был брошен в <b>' + data + '</b>');
                    $('.catapult-success-message').show('fast');

                    var inventory_cost = parseInt($('#inventoryCost').html());
                    var item_cost = $('#inventoryItem' + value).data('price')
                    //$('#inventoryCost').html(inventory_cost - item_cost);

                    var inventory_count = parseInt($('#inventoryCount').html());
                    $('#inventoryCount').html(inventory_count - 1);
                } else {
                    $('.catapult-error-message').show('fast');
                }
                $('.send-catapult').prop('disabled', true);
                $('#inventoryItem' + value).hide();
            }
        })
    });

    /* Продажа предметов в инвентаре */
    $('.sold-inventory-item-btn').click(function() {
        var parent = $(this).parent();
        $(this).prop('disabled', true);
        var item_id = $(parent).data('itemId');
        var price = $(parent).data('itemPrice');        
        console.log(item_id);
        console.log(price);
        $.ajax({
            type: "POST",
            url: "/users/sold/",
            data: {
                'id': item_id,
            },
            success: function(data) {                
                if (data == 'ok') {
                    var xp = parseInt($('#xpCounter').html());
                    $('#xpCounter').html(xp + price + 1);

                    var actions = parseInt($('#actionsCounter').html());
                    $('#actionsCounter').html(actions + 1);

                    var inventory_cost = parseInt($('#inventoryCost').html());
                    $('#inventoryCost').html(inventory_cost - price);

                    var inventory_count = parseInt($('#inventoryCount').html());
                    $('#inventoryCount').html(inventory_count - 1);

                    $(parent).hide(500);
                } else {
                    alert('Продать предмет не удалось');
                }
            }
        })
    });


    /* Открытие кейса */
    var casesItemsView = 1;
    var casesItemsOpen = setInterval(function() {
        $('#complectID' + casesItemsView).show('slow');
        casesItemsView++;
    }, 1500);

    setTimeout(function() {
        clearInterval(casesItemsOpen);        
    }, 10000);


    /* Star Wars */
    var starWarsMouseOver = false;
    $('.lightsaber').mouseover(function() {
        if (starWarsMouseOver == false) {
            $('.lightsaber').removeClass('lightsaber-0')
            .removeClass('lightsaber-1')
            .removeClass('lightsaber-2');

            starWarsMouseOver = true;
            $('.lightsaber').addClass('lightsaber-1');
            setTimeout(function () {
                if (starWarsMouseOver) {
                    $('.lightsaber').addClass('lightsaber-2');
                }                
            }, 500);
        }        
    });

    $('.lightsaber').mouseout(function() {
        if (starWarsMouseOver == true) {
            $('.lightsaber').removeClass('lightsaber-0')
            .removeClass('lightsaber-1')
            .removeClass('lightsaber-2');

            starWarsMouseOver = false;
            $('.lightsaber').addClass('lightsaber-0');
        }
    });


    /* ---------------- */

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