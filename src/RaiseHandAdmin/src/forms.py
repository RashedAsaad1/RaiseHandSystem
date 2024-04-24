from django import forms

class LoginForm(forms.Form):
    """
    A Django form for user login.

    This form has two fields: 'username' and 'password'. The 'username' field is a standard CharField, 
    while the 'password' field is a CharField with a PasswordInput widget, which means the input from 
    this field will be rendered as a password input (the input is masked).

    Attributes:
        username (CharField): The username field.
        password (CharField): The password field, with a PasswordInput widget.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)