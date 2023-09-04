$(document).ready(function () {
    $('#animanga_list').DataTable();


    $('selectedList').ready(function() {  
        if (selectedVal == "All") {
            $('.selectedList option[id=all]').attr('selected','selected');
        }
        else if (selectedVal == "Currently Watching") {
            $('.selectedList option[id=currentlyWatching]').attr('selected','selected');
        }
        else if (selectedVal == "Finished") {
            $('.selectedList option[id=finished]').attr('selected','selected');
        }
        else{
            $('.selectedList option[id=planned]').attr('selected','selected');
        }
    });


    $('.editItem').click(function(ev) {  
        var id = '#' + ev.target.id.substring(4)
        var rating = '#rating' + ev.target.id.substring(4)
        var list = $(id).find("option:selected").attr('value');
        
        if (list == 'Planned') {
            $(rating).prop('disabled', true);
        } 
        else {
            $(rating).prop('disabled', false);
        }
    });
    

    $('.listType').change(function(ev) {  
        var id = '#' + ev.target.id
        var rating = '#rating' + ev.target.id
        var list = $(id).find("option:selected").attr('value');
        
        if (list == 'Planned') {
            $(rating).prop('disabled', true);
        } 
        else {
            $(rating).prop('disabled', false);
        }
    });
})


