from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, FileField, MultipleFileField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()], render_kw={"placeholder": "Введите низвание"})
    content = TextAreaField("Содержание")
    files = MultipleFileField('Дабавьте пару фотографий (не больше 10!)', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    is_private = BooleanField("Черновик")
    submit = SubmitField('Применить')