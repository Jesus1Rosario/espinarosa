from django import forms
from .models import Producto
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen', 'stock', 'marca']
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class':'form-control'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'row': 3}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la marca'}),
        }
        

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False  # Aseguramos que los usuarios no sean administradores
        if commit:
            user.save()
        return user
