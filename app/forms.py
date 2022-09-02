from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange


class NewFood(FlaskForm):
    food_name = StringField('Food Name', validators=[DataRequired()])
    proteins = IntegerField('Proteins', validators=[DataRequired(), NumberRange(min=0)])
    carbs = IntegerField('Carbs', validators=[DataRequired(), NumberRange(min=0)])
    fats = IntegerField('Fats', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add')


class Date(FlaskForm):
    date = DateField()
    submit = SubmitField('Add')