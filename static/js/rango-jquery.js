/**
 * Created by Administrator on 2020-10-26.
 */
$(document).ready(function() {
    $("#about-btn").click( function(event) {
        alert("You clicked the button using jQuery!");
    });

    $(".ouch").click( function(event) {
        alert("You clicked me! ouch!");
    });

    $("p").hover( function() {
            $(this).css('color', 'red');
        },
        function() {
            $(this).css('color', 'blue');
        });

    $("#about-btn").addClass('btn btn-primary');

    $("#about-btn").click( function(event) {
        msgstr = $("#msg").html()
        msgstr = msgstr + "ooo"
        $("#msg").html(msgstr)
        });

    $('#likes').click(function(event){
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/rango/like/', {category_id: catid}, function(data){
            $('#like_count').html(data);
            $('#likes').hide();
        });});

    $('#suggestion').keyup(function(event){
        var query;
        query = $(this).val();
        $.get('/rango/suggest/', {suggestion: query}, function(data){
            $('#cats').html(data);
        });
    });
    var query;
    query = $(this).val();
    $.get('/rango/suggest/', {suggestion: query}, function(data){
        $('#cats').html(data);
    });
    $('.rango-add').click(function(){
        var catid = $(this).attr("data-catid");
        var url = $(this).attr("data-url");
        var title = $(this).attr("data-title");
        var me = $(this)
        $.get('/rango/add/',
            {category_id: catid, url: url, title: title}, function(data){
                $('#pages').html(data);
                me.hide();
            });
    });
});

