$(document).ready(function(){
    socket = io.connect(); // make the socket :^)

    socket.emit('join', socket_room); // join the right room
});