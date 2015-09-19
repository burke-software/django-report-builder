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

var check_report = false;
function check_if_report_done(report_id, task_id) {
	if (check_report != false ){
		$.get( "/report_builder/report/"+ report_id + "/check_status/" + task_id + "/", function( data ) {
			console.log(data);
			if (data.state == "SUCCESS") {
				window.location.href = data.link;
				clearInterval(check_report);
				check_report = false;
			}
		})
	}
}
function get_async_report(report_id) {
	$.get( "/report_builder/report/"+ report_id + "/download_file/xlsx/", function( data ) {
	    var task_id = data.task_id;
	    status = "loading"
	    check_report = setInterval( function(){ check_if_report_done(report_id, task_id); }, 2000 );
    });
}
