send_message = function (msg) {
    if (msg == null || msg.trim() === '') {
        return;
    }

    let to_send = {
        type: 'message',
        data: msg,
        room: socket_room
    };
    socket.emit('chat-message', to_send);
};
$('#messageform').submit(function (e) {
    e.preventDefault();

    let to_send = $('#messageform').serializeArray()[0].value;

    $.get('/checkgood/' + to_send, {}, function (data, status) {
        if (data === "True") {
            send_message(to_send);
        } else {
            function choose(choices) {
                let index = Math.floor(Math.random() * choices.length);
                return choices[index];
            }

            let pos = ["That's not very nice"];
            alert(choose(pos))
        }
    });

    $(this).closest('#messageform').find("input[type=text], textarea").val("");
});

$(document).ready(function () {
    // chat message recieved
    socket.on('chat-event', function (data) {
        switch (data['type']) {
            case 'message':
                console.log('new message');
                console.log(data);
                if (!data['moderator']) {
                    $("#messages").append("<p>" + data['username'] + ": " + data['data'] + "</p>");
                } else {
                    $("#messages").append("<p style='color:orangered'>" + data['username'] + ": " + data['data'] + "</p>");
                }

                break;
            case 'join':
                $("#messages").append("<p style='color:green'>" + data['message'] + " joined</p>");
                break;

            case 'disconnect':
                $("#messages").append("<p style='color:red'>" + data['message'] + " left</p>");
                break;
        }

        // scroll
        $("#messages").animate({scrollTop: $("#messages")[0].scrollHeight}, 500);

    });

    // debator join event
    socket.on('debator-join', function (data) {
        // remove from debator list
    });
    // debator leave event
    socket.on('debator-leave', function (data) {
        // add to debator list
    });
});

valid_text = function (text) {
    $.get('/checkgood/' + text, {}, function (data, status) {
        console.log(data === "True")
    });
};