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
});