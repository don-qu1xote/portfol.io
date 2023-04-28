from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, RadioField, FileField, \
    BooleanField
from wtforms.validators import DataRequired, Optional


class RegisterForm(FlaskForm):
    email = EmailField('Ваша почта', validators=[DataRequired()])
    password = PasswordField('Придумайте пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Ваше имя', validators=[DataRequired()])
    surname = StringField('Ваша фамилия', validators=[DataRequired()])
    username = StringField('Придумайте себе username', validators=[DataRequired()])
    speciality = RadioField('Выберите специальность:',
                            choices=[('Web-Разработчик', 'Web-Разработчик'), ('Data-science', 'Data-science'),
                                     ('Дизайнер', 'Дизайнер'), ('Game-dev', 'Game-dev'), ('Не указано', 'Прочее')],
                            default='Не указано')
    about = TextAreaField('Расскажите о себе:')
    GIT = StringField('Ссылка на Github')
    VK = StringField('Ссылка на VK')
    TG = StringField('Ссылка на Telegram')
    photo = FileField('Прикрепите вашу фотографию',
                      validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    surname = StringField('Ваша фамилия', validators=[DataRequired()])
    username = StringField('Придумайте себе username', validators=[DataRequired()])
    speciality = RadioField('Выберите специальность:',
                            choices=[('Web-Разработчик', 'Web-Разработчик'), ('Data-science', 'Data-science'), ('Дизайнер', 'Дизайнер'),
                                     ('Game-dev', 'Game-dev'), ('Не указано', 'Прочее')], default='Не указано')
    about = TextAreaField('Расскажите о себе:')
    GIT = StringField('Ссылка на Github')
    VK = StringField('Ссылка на VK')
    TG = StringField('Ссылка на Telegram')
    photo = FileField('Прикрепите вашу фотографию',
                      validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Изменить профиль!')

