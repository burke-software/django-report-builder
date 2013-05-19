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


function ajax_add_star(event, url) {    
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
