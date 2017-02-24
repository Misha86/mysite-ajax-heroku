$(function () {

    // ajax pagination
    $("#pages").on('click', ".pagination li a", function(event){
        event.preventDefault();
        var page = $(this);
        console.log(page.text())
        console.log(page.attr("href"))
        $.ajax({
            async: true,
            url: '/3d-max/galereya-robit/list-ajax/' + page.attr("href"),
            type: 'get',
            //data: {
            //    page : page.text()
            //},
            dataType: 'json',

            success: function (data) {
                $("#content").html(data.html_articles)
                $("#pages").html(data.html_page)

            },

            error : function(xhr, errmsg, err) {
                $('#result').html("<div class='container' data-alert><h1>Oops! We have encountered an error: " + xhr.status + errmsg +
                "</h1><a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                alert("Oops! We have encountered an error: " + err + " " + xhr.status + " " + errmsg )
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

    // search articles when push submit button
    $("#search").on('submit', function(event){
        event.preventDefault();
        var form = $(this);
        $.ajax({
            async: true,
            url: form.attr("action"),
            type: form.attr("method"),
            data: {
                q : $("#query").val()
            },
            dataType: 'json',

            success: function (data) {
                 console.log("success")
                $("#content").html(data.html_articles)
                $("#pages").html(data.html_page)
            },

            error : error_list
        });
    });

    // jquery ajax live search
    $('#search').keyup(function(event) {
        event.preventDefault();
        var form = $(this);
        $.ajax({
            async: true,
            url: form.attr("action"),
            type: form.attr("method"),
            data: {
                q : $("#query").val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: 'json',

            success: success_list,
            error : error_list
        });
    });

    $('#query').autocomplete({
       source: function(request, response){
        // организуем кроссдоменный запрос
        $.ajax({
          url: location,
          dataType: "json",
          // параметры запроса, передаваемые на сервер (последний - подстрока для поиска):
          data:{
            //featureClass: "P",
            //style: "full",
            //maxRows: 3,    // показать первые 12 результатов
            q: request.term
          },
          // обработка успешного выполнения запроса
          success: function(data){
              console.log(data.json_query)

            // приведем полученные данные к необходимому формату и передадим в предоставленную функцию response
            response($.map(data.json_query, function(item){
              return{
                //label: item.name + (item.adminName1 ? ", " + item.adminName1 : "") + ", " + item.countryName,
                value: item
              }
            }));
          }
        });
      },
      minLength: 2
    });


    function success_list(data) {
                $("#content").html(data.html_articles);
                $("#pages").html(data.html_page);
            };

    function error_list(xhr, errmsg, err) {
        $('#result').html("<div class='container' data-alert><h1>Oops! We have encountered an error: " + xhr.status + errmsg +
        "</h1><a href='#' class='close'>&times;</a></div>"); // add the error to the dom
        alert("Oops! We have encountered an error: " + err + " " + xhr.status + " " + errmsg)
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    };
});
