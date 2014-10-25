$(document).ready(function() {
	startInterval();
});

// declare interval and delay
var interval,delay = 10000;// miliseconds

var post_pic_html = "";

//Template html code for new post
var postTemplate = ""+
"<div class='well well-lg' id={{post_id}}>"+
	"<div class='row clearfix'>"+
		"<div class='col-md-4 column'>"+
			"<a href='/user_stream_{{post_user_id}}'>"+
				"<img src='picture/{{profile_id}}' alt='140x140' class='img-thumbnail'>"+
			"</a>"+
			"<p class='lead'>{{post_user_name}}</p>"+
		"</div>"+
		"<div class='col-md-8 column'>"+
			"<h2 class='media-heading'>{{post_subject}}</h2>"+
			"<p>{{post_date}}</p>"+
			"<br><pre class='media-body'>{{post_text}}</pre>"+
			"<br><div class='btn-group'><a href='delete_dislike/{{post_id}}'><button class='btn btn-default' type='button'>Like</button></a> <a href='dislike/{{post_id}}'><button class='btn btn-default' type='button'>Dislike</button></a> <button class='btn btn-default' data-toggle='collapse' data-target='#comment{{post_id}}' type='button'> Comment</button></div> <br>"+
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


var postPicTemplate = ""+
"<div class='well well-lg' id={{post_id}}>"+
	"<div class='row clearfix'>"+
		"<div class='col-md-4 column'>"+
			"<a href='/user_stream_{{post_user_id}}'>"+
				"<img src='picture/{{profile_id}}' alt='140x140' class='img-thumbnail'>"+
			"</a>"+
			"<p class='lead'>{{post_user_name}}</p>"+
		"</div>"+
		"<div class='col-md-8 column'>"+
			"<h2 class='media-heading'>{{post_subject}}</h2>"+
			"<p>{{post_date}}</p>"+
			"<br><pre class='media-body'>{{post_text}}</pre>"+
			"<img src='post_picture/{{post_id}}' class='img-thumbnail'>"+
			"<br><div class='btn-group'><a href='delete_dislike/{{post_id}}'><button class='btn btn-default' type='button'>Like</button></a> <a href='dislike/{{post_id}}'><button class='btn btn-default' type='button'>Dislike</button></a> <button class='btn btn-default' data-toggle='collapse' data-target='#comment{{post_id}}' type='button'> Comment</button></div> <br>"+
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

//Template html for new comment
var commentTemplate = ""+
"<pre class='media-body'>{{comment_user_name}}: {{comment_content}}"+
	"<a><i class='glyphicon glyphicon glyphicon-remove' name='remove_comment' id={{comment_id}}></i></a>"+
"</pre>"
;

// function that gets ran on interval
function runIntervalAjax(){
	var $content_part = $("#content_part");
	//window.alert($content_part.children().first().attr('id'));
	var latest_post_id = $content_part.children().first().attr('id');
	if(latest_post_id == null){
		latest_post_id = 0;
	}
	console.log(latest_post_id);

	$.ajax({
		url: '/check_update/'+latest_post_id,
		type: 'GET',
	})
	.done(function(data) {
		$.each( data, function(i, item) {
			var output = "";
			if(item['post_pic']==true){
				output = Mustache.render(postPicTemplate, item);
			}else{
				output = Mustache.render(postTemplate, item);
			}
			
			var comments = item['comments'];
			$.each(comments, function(i, comment_item) {
				 var commentOutput = Mustache.render(commentTemplate, comment_item);
				 console.log(commentOutput);
				 var comment_section = $(output).find("div[data-id=comment_part]");
				 console.log($(comment_section).attr('data-id'));
				 $(comment_section).append(commentOutput);
				 //$(commentOutput).prependTo($(comment_section));
			});
			$(output).hide().prependTo($content_part).slideDown(300);
        });

	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});
	
}

// function to stop interval
function stopInterval(){ // stop interval
      clearInterval(interval);
}

// function to start interval
function startInterval(){ // start interval
      runIntervalAjax();
      interval = setInterval(function(){
            runIntervalAjax();
      },delay);
}