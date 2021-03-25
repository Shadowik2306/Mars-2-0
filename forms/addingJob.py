from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class AddingJob(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    team_led_id = IntegerField('Team Leader id', validators=[DataRequired()])
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')