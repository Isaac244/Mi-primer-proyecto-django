from django import forms
#Libreria para validar formularios
#from django.contrib.auth.models import User
from users.models import User

class Registro(forms.Form):
    username = forms.CharField(
        required=True,
        min_length=5,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Nombre del usuario'
            }
        )
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'ejemplo@gamil.com'
            }
        )
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'placeholder': 'Contraseña'
            }
        )
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'placeholder': 'Confirmar Contraseña'
            }
        )
    )


    #FUNCIÓN VALIDAR USUARIO
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Usuario ya existe')
    
        return username
    
    #FUNCIÓN VALIDAR CORREO
    def clean_email(self):
        correo = self.cleaned_data.get('email')

        if User.objects.filter(email=correo).exists():
            raise forms.ValidationError('Correo ya existe')

        return correo
    
    #FUNCIÓN VALIDAR CONTRASEÑAS
    def clean(self):
        clean_data = super().clean()

        if clean_data.get('password2') != clean_data.get('password'):
            self.add_error('password2', 'Las contraseñas no coinciden')

    #FUNCIÓN METODO SAVE
    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password')
        )