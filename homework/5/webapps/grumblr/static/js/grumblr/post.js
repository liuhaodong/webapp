$(document).ready(function() {

	var $content_part = $("#content_part");
    var $post_button = $("#post_button");
    var $post_subject = $("#post_subject");
    var $post_text = $("#post_text");
    var $comment_button = $("button[data-id=comment_button]");
    var $remove_comment_button = $("i[name=remove_comment]");
    var $comment_part = $("div[data-id=comment_part]");


    //This part sets up ajax setting to use csrf token. This part of code is from Django Document.
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


    //Template html code for new post
    var postTemplate = ""+
    "<div class='well well-lg'>"+
    	"<div class='row clearfix'>"+
    		"<div class='col-md-4 column'>"+
    			"<a href='/user_stream_{{post_user_id}}'>"+
					"<img src='picture/{{profile_id}}' alt='140x140' class='img-thumbnail'>"+
    			"</a>"+
    			"<p class='lead'>{{post_user_name}}</p>"+
    		"</div>"+
    		"<div class='col-md-8 column'>"+
    			"<h2 class='media-heading'>{{post_subject}} <a><i class='glyphicon glyphicon glyphicon-remove' name='delete_post' id={{post_id}}></i></a></h2>"+
    			"<p>{{post_date}}</p>"+
    			"<br><pre class='media-body'>{{post_text}}</pre><br>"+
    			"<div class='btn-group'><a href='delete_dislike/{{post_id}}'><button class='btn btn-default' type='button'>Like</button></a> <a href='dislike/{{post_id}}'><button class='btn btn-default' type='button'>Dislike</button></a> <button class='btn btn-default' data-toggle='collapse' data-target='#comment{{post_id}}' type='button'> Comment</button></div> <br>"+
    			"<div id='comment{{post_id}}' class='collapse in'>"+
    				"<form accept-charset='utf-8'>"+
    					"<br><textarea class='form-control' rows=7 placeholder='Write your comment here!' name='comment' ></textarea><br>"+
    					"<button type='button' class='btn btn-primary' data-id='comment_button'>Comment</button>"+
    					"<input type='hidden' name='post_id'  value={{post_id}} >"+
    					""+
    				"</form><br>"+
    				"<div class='well' data-id='comment_part'>"+
    				"</div>"+
    			"</div>"+
    		"</div>"+
    	"</div>"+
    "</div>";

    function addPost(data){
    	var output = Mustache.render(postTemplate, data);

    	$(output).hide().insertAfter("#write_post").slideDown(300);
    		
    	//$("#content_part:first-child").after(output).fadeIn(1000);
    		
    	
       };

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

    //Remove Post!
    $content_part.on('click', 'i[name=delete_post]', function(event) {
    	var post_to_delete = $(this).parent().parent().parent().parent().parent();
    	var post_to_delete_id = $(this).attr('id');
    	$.ajax({
    		url: '/delete_post/'+post_to_delete_id,
    		type: 'GET',
    	})
    	.done(function() {
    		post_to_delete.slideUp(300, function(){post_to_delete.remove();})
    	})
    	.fail(function() {
    		console.log("error");
    	})
    	.always(function() {
    		console.log("complete");
    	});
    	
    	/* Act on the event */
    });

    //Template html for new comment
    var commentTemplate = ""+
    "<pre class='media-body'>{{comment_user_name}}: {{comment_content}}"+
    	"<a><i class='glyphicon glyphicon glyphicon-remove' name='remove_comment' id={{comment_id}}></i></a>"+
    "</pre>"
    ;

    function addComment(data){
    	var output = Mustache.render(commentTemplate, data);

    	$(output).hide().insertAfter("#write_post").slideDown(300);
    };

    $content_part.on('click', 'button[data-id=comment_button]', function(event) {
    	var newComment = {
    		post_id : $(this).siblings().filter($("input[name=post_id]")).val(),
    		comment : $(this).siblings().filter($("textarea[name=comment]")).val(),
    	};

    	var currentButton = $(this);

    	$.ajax({
    		url: '/add_comment',
    		type: 'POST',
    		dataType: 'json',
    		data: JSON.stringify(newComment),
    	})
    	.done(function(data) {
    		var output = Mustache.render(commentTemplate, data);
    		var comment_section = currentButton.parent().siblings().filter($("div[data-id=comment_part]"));
    		console.log(comment_section);
    		//$(output).prependTo($(this).parent());
    		$(output).hide().prependTo(comment_section).slideDown(300);
    	})
    	.fail(function() {
    		console.log("error");
    	})
    	.always(function() {
    		console.log("complete");
    	});
    	

    });


    $content_part.on('click', 'i[name=remove_comment]', function(event) {

    	var comment_to_delete = $(this).parent().parent();
    	var comment_id = $(this).attr('id');

    	$.ajax({
    		url: '/delete_comment/'+comment_id,
    		type: 'GET',
    	})
    	.done(function() {
    		comment_to_delete.slideUp(300, function(){comment_to_delete.remove();})
    	})
    	.fail(function() {
    		console.log("error");
    	})
    	.always(function() {
    		console.log("complete");
    	});

    });


});
