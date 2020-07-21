$(document).ready(function() {

    $('.commentButton').on('click', function() {

        var user_id = $(this).attr('user_id');
        var event_id = $(this).attr('post_id');
        this.style.backgroundColor = "#23DF1C";
        
        req = $.ajax({
            url : '/post/comment',
            type : 'POST',
            data : {  id : user_id , event_id : event_id,  }
        });
        req.done(function(data) {

            location.reload()
            $('#userNumber'+user_id).text(data.username)
            
            

        });
    

    });

});