$(function() {
    $('#basicMessage').submit(function() {
        $.ajax({
            url:'/',
            type:'POST',
            data:{
                operation:'insertItem',
                message:'Hello, Tom. ' + $('#theMessage').val() 
            },
            success:function() { alert('Your message was succesfully sent to timeline.'); },
            error:function() { alert('There was a problem sending your message to the timeline.'); }
        });
        return false;
    });
});
