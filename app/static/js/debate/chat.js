send_message = function(msg){
    let to_send = {
        type: 'message',
        data: msg,
        room: socket_room
    };
    socket.emit('chat-message', to_send);
};
$('#messageform').submit(function(e){
    e.preventDefault();

    let to_send = $('#messageform').serializeArray()[0].value;

    send_message(to_send);

    $(this).closest('#messageform').find("input[type=text], textarea").val("");
});

$(document).ready(function() {
    // chat message recieved
    socket.on('chat-event', function (data) {
        switch(data['type']){
            case 'message':
                console.log('new message');
                $("#messages").append("<p>" + data['username'] + ": " + data['data'] + "</p>");

                break;
            case 'join':
                $("#messages").append("<p style='color:green'>" + data['message'] + " joined</p>");
                break;

            case 'disconnect':
                $("#messages").append("<p style='color:red'>" + data['message'] + " left</p>");
                break;
        }
    });
});
//
// $(document).ready(function(){
//    initializeSocket();
//
//    console.log("chat");
// });
