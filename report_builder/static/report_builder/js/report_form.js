function expand_related(event, model, field, path, path_verbose) {
    if (event.target.tagName != 'LI') return;
    var element = $(event.target);
    if ( $(element).hasClass('tree_closed') ){
        $.get(  
            "/report_builder/ajax_get_related/",  
            {model: model, field: field, path: path, path_verbose: path_verbose},
            function(data){
                $(element).addClass('tree_expanded');
                $(element).removeClass('tree_closed');
                $(element).after('<li>' + data + '</li>');
            }  
        );
    } else{
        $(element).addClass('tree_closed');
        $(element).removeClass('tree_expanded');
        $(element).next().remove();
    }
}

function show_fields(event, model, field, path, path_verbose){
    $('.highlight').removeClass('highlight');
    $(event.target).addClass('highlight');
    $.get(  
        "/report_builder/ajax_get_fields/",  
        {model: model, field: field, path: path, path_verbose: path_verbose},
        function(data){
            $('#field_selection_div').html(data);
            
            enable_drag();
        }  
    );
}

function enable_drag() {
    $( ".draggable" ).draggable({
        connectToSortable: "#sortable",
        helper: "clone",
        revert: "invalid",
        zIndex: 10000
    });
    $( "#field_list_droppable" ).droppable({
        drop: function( event, ui ) {
            field = $.trim($(ui.draggable).text());
            name = $.trim($(ui.draggable).children().data('name'));
            path_verbose = $.trim($(ui.draggable).children().data('path_verbose'));
            path = $.trim($(ui.draggable).children().data('path'));
            
            if (name == '') return;
            
            total_forms = $('#id_displayfield_set-TOTAL_FORMS');
            i = total_forms.val();
            total_forms.val(parseInt(i)+1);
            
            row_html = '<tr><td><span style="cursor: move;" class="ui-icon ui-icon-arrowthick-2-n-s"></span></td>';
            row_html += '<td><input id="id_displayfield_set-'+i+'-path_verbose" name="displayfield_set-'+i+'-path_verbose" readonly="readonly" type="text" value="' + path_verbose + '"/></td>';
            row_html += '<td><input id="id_displayfield_set-'+i+'-field_verbose" name="displayfield_set-'+i+'-field_verbose" readonly="readonly" type="text" value="' + field + '"/><input id="id_displayfield_set-'+i+'-path" name="displayfield_set-'+i+'-path" type="hidden" value="' + path + '"/></td>';
            row_html += '<td><input id="id_displayfield_set-'+i+'-field" name="displayfield_set-'+i+'-field" type="hidden" value="' + name + '"/>'
            row_html += '<input id="id_displayfield_set-'+i+'-name" name="displayfield_set-'+i+'-name" type="text" value="' + name + '"/></td>';
            row_html += '<td><input type="text" name="displayfield_set-'+i+'-sort" class="small_input" id="id_displayfield_set-'+i+'-sort">';
            row_html += '<input type="checkbox" name="displayfield_set-'+i+'-sort_reverse" id="id_displayfield_set-'+i+'-sort_reverse"></td>';
            row_html += '<td><input type="text" name="displayfield_set-'+i+'-width" class="small_input" value="120" id="id_displayfield_set-'+i+'-width"></td>';
            row_html += '<td onclick="aggregate_tip()"><select id="id_displayfield_set-'+i+'-aggregate" name="displayfield_set-'+i+'-aggregate"><option selected="selected" value="">---------</option><option value="Count">Sum</option><option value="Ave">Ave</option><option value="Max">Max</option><option value="Min">Min</option></select></td>';
            row_html += '<td><input type="checkbox" name="displayfield_set-'+i+'-DELETE" id="id_displayfield_set-'+i+'-DELETE">';
            row_html += '<span class="hide_me"><input type="text" name="displayfield_set-'+i+'-position" value="999" id="id_displayfield_set-'+i+'-position"></span></td>';
            row_html += '</tr>';
            $('#field_list_table > tbody:last').append(row_html);
        }
    });
}

function refresh_preview() {
    $.post(  
        "/report_builder/ajax_preview/",  
        {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            report_id: $('#report_id').data('id'),
        },
        function(data){
            $('#tabs-3').html(data);
        }
    );
}

function aggregate_tip() {
    $('#tip_area').html('Aggregates can have unexpected behavior if used with sort order and the values in your search. To read more check out <a target="_blank" href="https://docs.djangoproject.com/en/dev/topics/db/aggregation/">Django Aggregation</a>')
    $('#tip_area').show('slow');
}

$(function() {
    enable_drag();
    $( "#tabs" ).tabs();
    $("#ui-id-3").click(refresh_preview);
    
    $('#field_list_table').sortable({
        containment: 'parent',
        zindex: 10,
        items: 'tbody tr',
        handle: 'td:first',
        update: function() {
            $(this).find('tbody tr').each(function(i) {
                if ($(this).find('input[id$=name]').val()) {
                    $(this).find('input[id$=position]').val(i+1);
                }
            });
        }
    });
    $( "#sortable" ).disableSelection();
});