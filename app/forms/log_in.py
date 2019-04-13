from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import input_required, length


class LogInForm(FlaskForm):
    username = StringField('Username:',
                             validators=[input_required('This field is required.'),
                                         length(3, 127)])
    password = PasswordField('Password:',
                             validators=[input_required('This field is required.'),
                                         length(7, 127)])

    submit = SubmitField("Log In")
