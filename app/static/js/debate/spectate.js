$(document).ready(function () {
    socket = io.connect(); // make the socket :^)

    socket.emit('join', socket_room); // join the right room

    update_overlay();

    socket.on('debate-status-update', function (data) {
        console.log(debate_status);
       debate_status = data;
       update_overlay();
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