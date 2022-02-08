from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])


class ProfileBaseForm(FlaskForm):
    first_name = StringField("first_name", validators=[DataRequired(), Length(max=20)])
    last_name = StringField("last_name", validators=[DataRequired(), Length(max=20)])
    age_years = IntegerField(
        "age_years", validators=[DataRequired(), NumberRange(min=18, max=100)]
    )
    interests = StringField("interests")
    city = StringField("city", validators=[DataRequired(), Length(max=30)])


class RegisterForm(ProfileBaseForm):
    email = StringField("email", validators=[DataRequired(), Email(), Length(max=40)])
    password = PasswordField(
        "password",
        validators=[DataRequired(), Length(min=8), EqualTo("password_again")],
    )
    password_again = PasswordField("password_again", validators=[DataRequired()])


class ProfileForm(ProfileBaseForm):
    pass
