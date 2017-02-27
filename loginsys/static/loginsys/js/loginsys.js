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


//Submit post on submit
$('#login').on('submit', function(event){
    event.preventDefault();
    //console.log("form submitted!")  // sanity check

    // AJAX for posting
    $.ajax({
        type : "POST", // http method
        async: true,
        url : "/auth/login_ajax/", // the endpoint
        data : {
            username : $('#username').val(),  // data sent with the post request
            password : $('#password').val()
        },
        dataType: 'json',

        // handle a successful response
        success : function(data) {
            if(data.form_valid) {
                console.log('succes');
                location.href = '/';
            } else {
                $('.errorlist').remove();
                var errorId = 'login_error';
                var invalidMessage;
                if (data.login_error_username && $('#username').val() == ''){
                    errorId = 'login_error_username';
                    invalidMessage = data.login_error_username;
                }
                else if (data.login_error_password && $('#password').val() == ''){
                    errorId = 'login_error_password';
                    invalidMessage = data.login_error_password;
                }
                else if (data.login_error_username_password && $('#username').val() == ''  && $('#password').val() == ''){
                    invalidMessage = data.login_error_username_password;
                }
                else if (data.login_error){
                    $('#password').val('');
                    invalidMessage = data.login_error;
                }

                $('#' + errorId).html("<label id=" + errorId + " class='control-label errorlist'><em>" +
                invalidMessage + "</em></label>");
                console.log(invalidMessage);
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
});



$(function() {
    var lang_cod = $('#lang_cod').text()
    //var cod = document.getElementById('cod').textContent;
    $.datepicker.setDefaults( $.datepicker.regional[ lang_cod ])
    $("#id_date_of_birth").datepicker(
        {changeMonth: true,
            changeYear: true,
            dateFormat: "yy-mm-dd",
            //showOn: "both",
            showWeek: true,
            yearRange: "1920:"

        });
});
