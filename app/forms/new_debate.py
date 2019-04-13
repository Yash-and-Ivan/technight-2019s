from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import input_required, length, equal_to


class NewDebateForm(FlaskForm):
    title = StringField('Debate Title:',
                        validators=[input_required('This field is required.'),
                                    length(3, 31)])
    description = StringField('Short Description:',
                              validators=[input_required('This field is required.'),
                                          length(0, 15)])

    password = PasswordField('Join Password:',
                             validators=[input_required('This field is required.'),
                                         length(2, 127)])
    password_confirm = PasswordField('Confirm Password:',
                                     validators=[input_required('This field is required.'),
                                                 equal_to('password', 'Your passwords should probably be the same'),
                                                 length(2, 127)])

    submit = SubmitField("Create Debate")
