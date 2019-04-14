$(document).ready(function(){
    socket = io.connect(); // make the socket :^)

    socket.emit('join', socket_room); // join the right room

    socket.on('debator-join', function(data){
        $("#debator-list").append('<button onclick="questionRoutine_setup(\'' + data + '\')" id="' + data + '" class="btn btn-light">' + data + '</button>')
    });

    socket.on('debator-leave', function(data){
        $("#" + data).remove(); // remove
        if(cur_questioned === data){
            $("#question-area").hide();
        }
    });



});

questionRoutine_setup = function(username){
    cur_questioned = username;
    $("#question-area").show();

    $("#selected-user").text(username);

};

askquestion = function(){
  let data = {};

  data.question = $("#question-asked").val();
  data.time = $("#time-limit").val();
  data.user = cur_questioned;
  data.room = socket_room;

  console.log(data);
};

$(document).on('input', '#time-limit', function() {
    $('#timer-value').html( $(this).val() + "s");
});