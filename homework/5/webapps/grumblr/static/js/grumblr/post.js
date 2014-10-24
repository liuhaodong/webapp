$(document).ready(function() {

    var $post_button = $("#post_button");
    var $post_subject = $("#post_subject");
    var $post_text = $("#post_text");

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var postTemplate = ""+
    "<div class='well well-lg'>"+
    	"<div class='row clearfix'>"+
    		"<div class='col-md-4 column'>"+
    			"<a href='/user_stream_{{post_user_id}}'>"+
					"<img src='picture/{{profile_id}}' alt='140x140' class='img-thumbnail'>"+
    			"</a>"+
    			"<p class='lead'>{{post_user_name}}</p>"+
    		"</div>"+
    		"<div class='col-md-8 column'>{{post_subject}}{{post_text}}</div>"+
    	"</div>"+
    "</div>";

    function addPost(data){
    	$('#content_part').append(Mustache.render(postTemplate, data));
    }

    $post_button.click(function() {

        var newPost = {
            subject: $post_subject.val(),
            post: $post_text.val(),
        };

        $.ajax({
            url: '/add_post',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify(newPost),
        })

        .done(function(data) {
        	addPost(data);
        })

        .fail(function() {
                console.log("error");
            })
        .always(function() {
                console.log("complete");
            });

    });

});
