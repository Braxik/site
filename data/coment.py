from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class AddComForm(FlaskForm):
    content = StringField('Write comment', validators=[DataRequired()])
    submit = SubmitField('Submit')