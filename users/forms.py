# users/forms.py
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib.auth.models import Group


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

    error_messages = {
        'invalid_login': "E-mail ou senha incorretos. Tente novamente.",
        'inactive': "Esta conta está inativa.",
    }

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            # Autentica o usuário pelo email
            self.user_cache = authenticate(username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'phone', 'city', 'description', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'name': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'city': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'description': forms.Textarea(attrs={'class': 'w-full mt-1 p-2 border rounded', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
        }


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(
        attrs={'class': 'w-full mt-1 p-2 border rounded'}))
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput(
        attrs={'class': 'w-full mt-1 p-2 border rounded'}))

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'phone', 'city']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'name': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
            'city': forms.Select(attrs={'class': 'w-full mt-1 p-2 border rounded'}),
        }
        error_messages = {
            'username': {'required': 'Este campo é obrigatório.'},
            'name': {'required': 'Este campo é obrigatório.'},
            'email': {'required': 'Este campo é obrigatório.'},
            'phone': {'required': 'Este campo é obrigatório.'},
            'city': {'required': 'Este campo é obrigatório.'},
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Verifica se o grupo "Usuário Normal" existe, caso contrário, cria-o
            normal_user_group, created = Group.objects.get_or_create(name='Usuário Normal')
            user.groups.add(normal_user_group)
        return user
