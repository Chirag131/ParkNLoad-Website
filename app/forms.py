from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class BaseProfileForm(FlaskForm):
    name = StringField('Name', render_kw={'readonly': True})
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email',render_kw={'readonly': True} )


    submit = SubmitField('Save')