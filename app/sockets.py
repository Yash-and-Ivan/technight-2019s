from flask_socketio import SocketIO, join_room, emit, rooms
from flask import request
from flask_login import current_user
from app.models import Debate, db

socketio = SocketIO()


@socketio.on('connect')
def connect():
    print('New client has connected')


@socketio.on('disconnect')
def disconnect():
    print(rooms(request.sid))
    ret = {
        'type': 'disconnect',
        'message': current_user.username
    }
    for room in rooms(request.sid):
        ret['room'] = room

        debate = Debate.query.filter_by(url=room).first()

        if debate is None:
            continue

        if debate.created_by_id == current_user.id:
            debate.active = False
            db.session.commit()

            emit('debate-status-update', False, broadcast=True, room=room)

        else:
            emit('chat-event', ret, broadcast=True, room=room)

    if current_user.active:
        current_user.active = False
        debate = Debate.query.get(current_user.active_in_id)
        current_user.active_in_id = None
        emit('debator-leave', current_user.username, broadcast=True, room=debate.url)


    db.session.commit()
    print('A client has disconnected')


@socketio.on('join')
def join(data):
    print('Client joined room %s' % data)

    # check if client moderates the room
    debate = Debate.query.filter_by(url=data).first()
    assert(debate is not None)

    if debate.created_by_id == current_user.id:
        # set debate status to active and don't tell anyone
        debate.active = True
        db.session.commit()

        emit('debate-status-update', True, broadcast=True, room=data)

    else:
        ret = {
            'type': 'join',
            'message': current_user.username,
            'room': data
        }
        emit('chat-event', ret, broadcast=True, room=data)

    join_room(data)


@socketio.on('chat-message')
def message(data):
    data['username'] = current_user.username
    debate = Debate.query.filter_by(url=data['room']).first()
    if debate.created_by_id == current_user.id:
        data['moderator'] = True
    else:
        data['moderator'] = False
    emit('chat-event', data, broadcast=True, room=data['room'])


@socketio.on('debator-join')
def debator_join(room):
    # debator join
    current_user.active = True
    debate = Debate.query.filter_by(url=room).first()
    current_user.active_in_id = debate.id
    db.session.commit()

    emit('debator-join', current_user.username, room=room, broadcast=True)

    print("Debator joined")
