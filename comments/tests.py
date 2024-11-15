from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from users.models import User
from events.models import Event, Location
from .models import Comment
from .forms import CommentForm

class CommentModelTest(TestCase):
    def setUp(self):
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        # Criar localização de teste
        self.location = Location.objects.create(
            cep='63050-000',
            street='Rua Teste',
            number='123',
            neighborhood='Centro',
            city='Juazeiro do Norte',
            state='CE'
        )
        
        # Criar evento de teste
        self.event = Event.objects.create(
            title='Evento Teste',
            description='Descrição teste',
            date=timezone.now(),
            time=timezone.now().time(),
            location=self.location,
            max_capacity=100,
            creator=self.user
        )
        
        # Criar comentário de teste
        self.comment = Comment.objects.create(
            comment='Comentário teste',
            author=self.user,
            event=self.event
        )

    def test_comment_creation(self):
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertEqual(str(self.comment), 'Comentário teste')
        
    def test_comment_fields(self):
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.event, self.event)
        self.assertEqual(self.comment.comment, 'Comentário teste')


class CommentViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        # Criar localização de teste
        self.location = Location.objects.create(
            cep='63050-000',
            street='Rua Teste',
            number='123',
            neighborhood='Centro',
            city='Juazeiro do Norte',
            state='CE'
        )
        
        # Criar evento de teste
        self.event = Event.objects.create(
            title='Evento Teste',
            description='Descrição teste',
            date=timezone.now(),
            time=timezone.now().time(),
            location=self.location,
            max_capacity=100,
            creator=self.user
        )
        
        self.comment = Comment.objects.create(
            comment='Comentário teste',
            author=self.user,
            event=self.event
        )

    def test_comment_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        # Adiciona o evento_id como parâmetro na URL
        response = self.client.post(
            reverse('comments'),
            {'comment': 'Novo comentário', 'event': self.event.id}
        )
        self.assertEqual(response.status_code, 302)  # Deve redirecionar após criar
        
    def test_comment_create_view_requires_login(self):
        response = self.client.get(reverse('comments'))
        expected_url = f'/accounts/login/?next={reverse("comments")}'
        self.assertRedirects(
            response, 
            expected_url, 
            fetch_redirect_response=False  # Não tenta acessar a página de redirecionamento
        )
        
    def test_comment_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('comment_edit', kwargs={'pk': self.comment.pk}),
            {'comment': 'Comentário atualizado', 'event': self.event.id}
        )
        self.assertEqual(response.status_code, 302)  # Deve redirecionar após atualizar
        
    def test_comment_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('comment_delete', kwargs={'pk': self.comment.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redireciona após deletar


class CommentFormTest(TestCase):
    def test_comment_form_valid(self):
        form_data = {'comment': 'Este é um comentário de teste'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_comment_form_invalid(self):
        form_data = {'comment': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
