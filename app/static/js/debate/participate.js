$(document).ready(function () {
    socket = io.connect(); // make the socket :^)

    socket.emit('join', socket_room); // join the right room
    socket.emit('debator-join', socket_room); // debator has joined

    update_overlay();

    socket.on('debate-status-update', function (data) {
        console.log(debate_status);
       debate_status = data;
       update_overlay();
    });

    socket.on('debator-join', function(data){
        if(username === data) {
            $("#debator-list").append('<button id="' + data + '" class="btn btn-primary">' + data + ' (you)</button>')
        } else {
            $("#debator-list").append('<button id="' + data + '" class="btn btn-light">' + data + '</button>')
        }
    });

    socket.on('debator-leave', function(data){
       $("#" + data).remove() // remove
    });

});

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