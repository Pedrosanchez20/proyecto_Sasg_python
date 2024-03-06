from django import forms

class LoginForm(forms.Form):
    idusuario = forms.IntegerField(label='ID de Usuario')
    contrasena = forms.CharField(widget=forms.PasswordInput)