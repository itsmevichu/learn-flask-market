from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField ,ValidationError
from wtforms.validators import Length, Email, EqualTo, DataRequired
from market.models import User

class Register_form(FlaskForm):

    def validate_userName(self,userName_to_check):
        user= User.query.filter_by(userName=userName_to_check.data).first()
        if user:
            raise ValidationError(f'The Username: {user.userName} already exists.')
    
    def validate_email_address(self,email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError(f'The email address: {email.email_address} already exists.')

    userName= StringField(label='userName', validators=[Length(min=2,max=25),DataRequired()])
    email_address= StringField(label='email', validators=[Email(),DataRequired()])
    password1= PasswordField(label='password1', validators=[Length(min=6),DataRequired()])
    password2= PasswordField(label='password2',validators=[EqualTo('password1'),DataRequired()])
    submit= SubmitField(label='Create Account')
 
class Login_form(FlaskForm):
    userName= StringField(label='userName', validators=[DataRequired()])
    password = PasswordField(label='password',validators=[DataRequired()])
    submit= SubmitField(label='Sign In')

class PurchaseItem_Form(FlaskForm):
    submit=SubmitField(label="Confirm Buy")

class SellItem_Form(FlaskForm):
    submit=SubmitField(label="Sell")