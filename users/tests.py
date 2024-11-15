from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from .forms import UserCreationForm, UserProfileForm, EmailAuthenticationForm
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile


class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user_data = {
            'username': 'testuser',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '88999999999',
            'city': 'JDO',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        # Usar get_or_create ao invés de create
        self.normal_group, _ = Group.objects.get_or_create(name='Usuário Normal')

    def test_user_registration(self):
        response = self.client.post(reverse('register'), self.test_user_data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após registro
        self.assertTrue(User.objects.filter(email=self.test_user_data['email']).exists())
        user = User.objects.get(email=self.test_user_data['email'])
        self.assertTrue(user.groups.filter(name='Usuário Normal').exists())

    def test_user_login(self):
        # Criar usuário primeiro
        user = User.objects.create_user(
            username=self.test_user_data['username'],
            email=self.test_user_data['email'],
            password=self.test_user_data['password1']
        )
        
        # Tentar login
        login_data = {
            'username': self.test_user_data['email'],
            'password': self.test_user_data['password1']
        }
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após login

    def test_user_logout(self):
        # Criar e logar usuário
        user = User.objects.create_user(
            username=self.test_user_data['username'],
            email=self.test_user_data['email'],
            password=self.test_user_data['password1']
        )
        self.client.login(username=self.test_user_data['email'], password=self.test_user_data['password1'])
        
        # Testar logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirecionamento após logout

    def test_profile_update(self):
        # Criar e logar usuário
        user = User.objects.create_user(
            username=self.test_user_data['username'],
            email=self.test_user_data['email'],
            password=self.test_user_data['password1']
        )
        self.client.login(username=self.test_user_data['email'], password=self.test_user_data['password1'])
        
        # Dados para atualização
        update_data = {
            'username': 'updateduser',
            'name': 'Updated Name',
            'email': 'updated@example.com',
            'phone': '88988888888',
            'city': 'CRT',
            'description': 'Test description'
        }
        
        response = self.client.post(reverse('profile'), update_data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após atualização
        updated_user = User.objects.get(id=user.id)
        self.assertEqual(updated_user.username, 'updateduser')

    def test_view_user_profile(self):
        user = User.objects.create_user(
            username=self.test_user_data['username'],
            email=self.test_user_data['email'],
            password=self.test_user_data['password1']
        )
        
        response = self.client.get(reverse('user_profile', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')

    def test_invalid_registration(self):
        # Testar registro com senhas diferentes
        invalid_data = self.test_user_data.copy()
        invalid_data['password2'] = 'differentpass'
        response = self.client.post(reverse('register'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Permanece na página com erro
        self.assertFalse(User.objects.filter(email=invalid_data['email']).exists())

    def test_invalid_login(self):
        # Testar login com credenciais inválidas
        invalid_login = {
            'username': 'nonexistent@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(reverse('login'), invalid_login)
        self.assertEqual(response.status_code, 200)  # Permanece na página com erro

    def test_profile_required_login(self):
        # Tentar acessar perfil sem estar logado
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirecionamento para login

class UserFormsTests(TestCase):
    def test_user_creation_form(self):
        form_data = {
            'username': 'testuser',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '88999999999',
            'city': 'JDO',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_profile_form(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        form_data = {
            'username': 'testuser',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '88999999999',
            'city': 'JDO',
            'description': 'Test description'
        }
        form = UserProfileForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())
