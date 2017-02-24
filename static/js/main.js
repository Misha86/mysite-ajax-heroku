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
                $("#form-massage").html(data.html_form)

                if (data.html_messages) {
                    $("#messages").html(data.html_messages)
                }
                else {
                    $("#messages").html('')
                };
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