from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=4, max=25,
                                              message='Це поле має бути довжиною між 4 та 25 символів'),
                                       DataRequired(message='Це поле обовязкове'),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Username must have only '
                                              'letters, numbers, dots or '
                                              'underscores')])

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[Length(min=6,
                                                message='Це поле має бути довжиною більше 6 символів'),
                                         DataRequired(message='Це поле обовязкове')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f"User with {email.data} email already registered.")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f"Username already in use.")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddPost(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content')
    submit = SubmitField('Add Post')


class UpdatePost(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Content')
    submit = SubmitField('Add Post')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=4, max=25,
                                              message='Це поле має бути довжиною між 4 та 25 символів'),
                                       DataRequired(message='Це поле обовязкове'),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Username must have only '
                                              'letters, numbers, dots or '
                                              'underscores')])

    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = StringField('About me')
    last_seen = StringField('Last seen')
    password = PasswordField('Password',
                             validators=[Length(min=6,
                                                message='Це поле має бути довжиною більше 6 символів'),
                                         DataRequired(message='Це поле обовязкове')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f"That email is taken. Please choose a different one.")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f"That username is taken. Please choose a different one.")
