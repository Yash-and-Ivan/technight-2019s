$(document).ready(function () {
    socket = io.connect(); // make the socket :^)

    socket.emit('join', socket_room); // join the right room

    update_overlay();

    socket.on('debate-status-update', function (data) {
        console.log(debate_status);
        debate_status = data;
        update_overlay();
    });

    socket.on('debator-join', function (data) {
        $("#debator-list").append('<button id="' + data + '" class="btn btn-light">' + data + '</button>')
    });

    socket.on('debator-leave', function (data) {
        $("#" + data).remove() // remove
    });

    socket.on('new-question', function(data){
        $("#question-area").hide();
        $("#question-show").show();
        $("#current-question").text(data['question']);
        timer = parseInt(data['time']);
        $("#current-timer").text(data['time'] + 's');
        $("#current-questioned").text(data['user']);

        window.setTimeout(do_timer, 1000);
    });

    socket.on('end-question', function(data){
        question_in_progress = false;
        $("#question-show").hide();
    });

});

do_timer = function(){
    timer--;
    if(timer == 0){
        // send out the signal that ends the question time
        endquestion();
    }
    $("#current-timer").text(timer + 's');
    if(timer !== 0) {
        window.setTimeout(do_timer, 1000);
    }
};

update_overlay = function () {
    if (debate_status) {
        $("#spectate-overlay").hide()
    } else {
        $("#spectate-overlay").show()
    }
};

$(document).ready(function () {
    update_overlay();
});