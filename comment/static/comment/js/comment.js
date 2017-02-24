// Acquiring the token is straightforward using jQuery
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
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(function () {
    $('#form-massage').on('submit', function(event){
        event.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            type: form.attr("method"),
            data: form.serialize(),
            dataType: 'json',

            success: function (data) {
                $("#form-massage").html(data.html_form);

                if (data.form_is_valid) {
                    $("#comments_list").html(data.html_comments);
                }

                if (data.html_messages) {
                    $("#messages").html(data.html_messages);
                }
                else {
                    $("#messages").html('')
                }
            },

            error : function(xhr, errmsg, err) {
                $('#result').html("<div class='container' data-alert><h1>Oops! We have encountered an error: " + xhr.status + errmsg +
                "</h1><a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                alert("Oops! We have encountered an error: " + err + " " + xhr.status + " " + errmsg )
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        return false;
    });
});