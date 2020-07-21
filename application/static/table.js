$(document).ready(function() {

    $('.updateButton').on('click', function() {

        var user_id = $(this).attr('user_id');
        var event_id = $(this).attr('event_id');
        this.style.backgroundColor = "#23DF1C";
        
        req = $.ajax({
            url : '/post/event/update',
            type : 'POST',
            data : {  id : user_id , event_id : event_id }
        });
        req.done(function(data) {

            location.reload()
            $('#userNumber'+user_id).text(data.username)
            
            

        });
    

    });

});

$(document).ready(function() {

    $('.warningButton').on('click', function() {

        var user_id = $(this).attr('user_id');
        var event_id = $(this).attr('event_id');
        this.style.backgroundColor = "#23DF1C";
        
        req = $.ajax({
            url : '/post/event/warning',
            type : 'POST',
            data : {  id : user_id , event_id : event_id }
        });
        req.done(function(data) {

            location.reload()
            $('#userNumber'+user_id).text(data.username)
            
            

        });
    

    });

});



function refreshPage () {
    var page_y = $( document ).scrollTop();
    window.location.href = window.location.href;
}
window.onload = function () {
    setTimeout(refreshPage, 35000);
    if ( window.location.href.indexOf('page_y') != -1 ) {
        var match = window.location.href.split('?')[1].split("&")[0].split("=");
        $('html, body').scrollTop( match[1] );
    }
}
