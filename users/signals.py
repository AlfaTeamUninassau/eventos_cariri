# users/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from events.models import Event, EventImage, Location
from comments.models import Comment
from reviews.models import Review

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Cria o grupo "Usuário Normal" se não existir
    normal_user_group, created = Group.objects.get_or_create(name='Usuário Normal')
    
    if created:
        # Adiciona permissões ao grupo "Usuário Normal"
        normal_permissions = [
            # Permissões de eventos
            Permission.objects.get(codename='add_event'),
            Permission.objects.get(codename='change_event'),
            Permission.objects.get(codename='delete_event'),
            Permission.objects.get(codename='view_event'),
            Permission.objects.get(codename='add_eventimage'),
            Permission.objects.get(codename='change_eventimage'),
            Permission.objects.get(codename='delete_eventimage'),
            Permission.objects.get(codename='view_eventimage'),
            Permission.objects.get(codename='add_location'),
            Permission.objects.get(codename='change_location'),
            Permission.objects.get(codename='delete_location'),
            Permission.objects.get(codename='view_location'),
            # Permissões de comentários
            Permission.objects.get(codename='add_comment'),
            Permission.objects.get(codename='change_comment'),
            Permission.objects.get(codename='delete_comment'),
            Permission.objects.get(codename='view_comment'),
            # Permissões de reviews
            Permission.objects.get(codename='add_review'),
            Permission.objects.get(codename='change_review'),
            Permission.objects.get(codename='view_review'),
        ]
        
        # Adiciona as permissões ao grupo "Usuário Normal"
        normal_user_group.permissions.set(normal_permissions)
    
    # Cria o grupo "Administrador" se não existir
    admin_group, created = Group.objects.get_or_create(name='Administrador')
    
    if created:
        # Adiciona todas as permissões ao grupo "Administrador"
        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)