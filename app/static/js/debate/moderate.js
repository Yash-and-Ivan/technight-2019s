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
endquestion = function(){
    socket.emit('end-question', socket_room);
};

questionRoutine_setup = function(username){
    if(question_in_progress){
        return;
    }

    cur_questioned = username;
    $("#question-area").show();
    $("#question-show").hide();

    $("#selected-user").text(username);

};

askquestion = function(){
  let data = {};

  data.question = $("#question-asked").val();
  data.time = $("#time-limit").val();
  data.user = cur_questioned;
  data.room = socket_room;

  question_in_progress = true;
  socket.emit('new-question', data);
};

$(document).on('input', '#time-limit', function() {
    $('#timer-value').html( $(this).val() + "s");
});