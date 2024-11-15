from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from events.models import Event, Location
from reviews.models import Review

User = get_user_model()

class ReviewViewsTest(TestCase):
    def setUp(self):
        # Criar um usuário para os testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        # Criar uma localização para o evento
        self.location = Location.objects.create(
            cep='63180000',
            street='Test Street',
            number='123',
            neighborhood='Test Neighborhood',
            city='Test City',
            state='CE'
        )
        
        # Criar um evento para testar as reviews
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date='2024-12-31',
            time='20:00:00',
            category='Cultura',
            location=self.location,
            max_capacity=100,
            creator=self.user
        )
        
        # Criar uma review para testes de atualização/deleção
        self.review = Review.objects.create(
            event=self.event,
            user=self.user,
            rating=5,
            comment='Great event!'
        )
        
        self.client = Client()

    def test_create_review(self):
        # Criar um novo usuário para o teste de criação
        # (já que o primeiro usuário já tem uma review criada no setUp)
        new_user = User.objects.create_user(
            username='newuser',
            email='new@test.com',
            password='testpass123'
        )
        
        # Fazer login com o novo usuário
        self.client.login(email='new@test.com', password='testpass123')
        
        # Dados da review
        review_data = {
            'rating': 4,
            'comment': 'Good event!'
        }
        
        # Tentar criar uma nova review
        response = self.client.post(
            reverse('review_create', kwargs={'event_id': self.event.id}),
            review_data
        )
        
        # Verificar se foi redirecionado para a página do evento
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('event_detail', kwargs={'pk': self.event.id}))
        
        # Verificar se a review foi criada
        self.assertTrue(Review.objects.filter(user=new_user, event=self.event).exists())

    def test_cannot_create_duplicate_review(self):
        # Fazer login com o usuário que já tem uma review
        self.client.login(email='test@test.com', password='testpass123')
        
        # Tentar criar outra review para o mesmo evento
        review_data = {
            'rating': 3,
            'comment': 'Trying to add another review'
        }
        
        response = self.client.post(
            reverse('review_create', kwargs={'event_id': self.event.id}),
            review_data
        )
        
        # Verificar se a requisição não foi bem sucedida
        self.assertEqual(response.status_code, 400)  # ou outro código apropriado
        
        # Verificar se ainda existe apenas uma review deste usuário para este evento
        self.assertEqual(
            Review.objects.filter(user=self.user, event=self.event).count(),
            1
        )

    def test_update_review(self):
        # Fazer login
        self.client.login(email='test@test.com', password='testpass123')
        
        # Dados atualizados da review
        updated_data = {
            'rating': 3,
            'comment': 'Updated comment'
        }
        
        # Tentar atualizar a review
        response = self.client.post(
            reverse('review_update', kwargs={'pk': self.review.pk}),
            updated_data
        )
        
        # Verificar se foi redirecionado para a página do evento
        self.assertEqual(response.status_code, 302)
        
        # Verificar se a review foi atualizada
        updated_review = Review.objects.get(pk=self.review.pk)
        self.assertEqual(updated_review.rating, 3)
        self.assertEqual(updated_review.comment, 'Updated comment')

    def test_delete_review(self):
        # Fazer login
        self.client.login(email='test@test.com', password='testpass123')
        
        # Tentar deletar a review
        response = self.client.post(
            reverse('review_delete', kwargs={'pk': self.review.pk})
        )
        
        # Verificar se foi redirecionado para a página do evento
        self.assertEqual(response.status_code, 302)
        
        # Verificar se a review foi deletada
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(pk=self.review.pk)

    def test_unauthorized_access(self):
        # Criar outro usuário
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@test.com',
            password='testpass123'
        )
        
        # Fazer login com o outro usuário
        self.client.login(email='other@test.com', password='testpass123')
        
        # Tentar atualizar a review de outro usuário
        response = self.client.post(
            reverse('review_update', kwargs={'pk': self.review.pk}),
            {'rating': 1, 'comment': 'Bad attempt'}
        )
        
        # Verificar se o acesso foi negado
        self.assertEqual(response.status_code, 404)
