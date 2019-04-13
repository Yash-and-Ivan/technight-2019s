from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import equal_to, input_required, length


class SignUpForm(FlaskForm):
    username = StringField('Username:',
                           validators=[input_required('This field is required.'),
                                       length(3, 127)])
    password = PasswordField('Password:',
                             validators=[input_required('This field is required.'),
                                         length(7, 127)])
    password_confirm = PasswordField('Repeat Password:',
                                     validators=[input_required('This field is required.'),
                                                 equal_to('password', 'Your passwords should probably be the same'),
                                                 length(7, 127)])

    submit = SubmitField("Sign Up")
