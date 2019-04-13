from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import input_required, length


class NewDebateForm(FlaskForm):
    title = StringField('Debate Title:',
                             validators=[input_required('This field is required.'),
                                         length(7, 31)])
    description = StringField('Short Description:',
                             validators=[input_required('This field is required.'),
                                         length(0, 15)])

    submit = SubmitField("Create Debate")
