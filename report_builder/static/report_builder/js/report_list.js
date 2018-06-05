$ = django.jQuery;
// place this in your static files folder, in:
//    <static>/report_builder/js/report_form.js

// initialize path prefix.
path_prefix = ""

// get current path
current_path =  window.location.pathname;

// where is "/report_builder"?
root_index = current_path.indexOf( "/report_builder" );

// other than 0?
if ( root_index > 0 )
{

    // yes.  Get all text from start to that location, store it as path_prefix.
    path_prefix = current_path.substring( 0, root_index );

}
else
{

    // no - set path_prefix to "".
    path_prefix = "";

}

/* Taken from https://docs.djangoproject.com/en/dev/ref/contrib/csrf/ */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function ajax_add_star(event, url) {

	// Setup CSRF Token
	var csrftoken = getCookie('csrftoken');
	$.ajaxSetup({
		crossDomain: false, // obviates need for sameOrigin test
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type)) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

    $.post(
        url,
	{},
        function(data){
	    if (data == 'True' ) {
		$(event).html('<img style="width: 26px; margin: -6px;" src="/static/report_builder/img/star.png">');
	    } else {
		$(event).html('<img style="width: 26px; margin: -6px;" src="/static/report_builder/img/unstar.png">');
	    }
        }
    );}
