from django import forms
from .models import Comments
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))
    #captcha = CaptchaField(label='Verification code')

class RegisterForm(forms.Form):
    gender = (
        ('male', "Male"),
        ('female', "Female"),
    )

    tags_choice = (
        ('N/A',"N/A"),
        ('adventure',"Adventure"),
        ('ancient',"Ancient"),
        ('educational',"Educational"),
        ('fighting',"Fighting"),
        ('racing',"Racing"),
        ('sports',"Sports"),
        ('wargame',"Wargame"),
        ('zombies',"Zombies"),
    )

    community_choice =(
        ('N/A',"N/A"),
        ('gamechat',"GameChat"),
        ('gamequestions',"GameQuestions"),
        ('bugs',"Bugs"),
        ('find users',"FindUsers"),
        ('avatars',"Avatars"),
        ('stats',"Stats")
    )

    username = forms.CharField(label="Username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Comfirm Passwword", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label='Gender', choices=gender)
    tag = forms.ChoiceField(label='Tag', choices=tags_choice)
    community = forms.ChoiceField(label='Community', choices=community_choice)
    #captcha = CaptchaField(label='验证码')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_publisher', 'comment_text']

