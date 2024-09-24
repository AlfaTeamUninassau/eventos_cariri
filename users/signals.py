from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from events.models import Event
from comments.models import Comment
from reviews.models import Review

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # Cria o grupo "Usuário Normal" se não existir
    normal_user_group, created = Group.objects.get_or_create(name='Usuário Normal')
    
    if created:
        # Define as permissões para o grupo "Usuário Normal"
        event_content_type = ContentType.objects.get_for_model(Event)
        comment_content_type = ContentType.objects.get_for_model(Comment)
        review_content_type = ContentType.objects.get_for_model(Review)
        
        normal_permissions = [
            Permission.objects.get_or_create(codename='add_event', name='Can add event', content_type=event_content_type)[0],
            Permission.objects.get_or_create(codename='change_event', name='Can change event', content_type=event_content_type)[0],
            Permission.objects.get_or_create(codename='delete_event', name='Can delete event', content_type=event_content_type)[0],
            Permission.objects.get_or_create(codename='view_event', name='Can view event', content_type=event_content_type)[0],
            Permission.objects.get_or_create(codename='add_comment', name='Can add comment', content_type=comment_content_type)[0],
            Permission.objects.get_or_create(codename='change_comment', name='Can change comment', content_type=comment_content_type)[0],
            Permission.objects.get_or_create(codename='delete_comment', name='Can delete comment', content_type=comment_content_type)[0],
            Permission.objects.get_or_create(codename='view_comment', name='Can view comment', content_type=comment_content_type)[0],
            Permission.objects.get_or_create(codename='add_review', name='Can add review', content_type=review_content_type)[0],
            Permission.objects.get_or_create(codename='change_review', name='Can change review', content_type=review_content_type)[0],
            Permission.objects.get_or_create(codename='view_review', name='Can view review', content_type=review_content_type)[0],
        ]
        
        # Adiciona as permissões ao grupo "Usuário Normal"
        normal_user_group.permissions.set(normal_permissions)
    
    # Cria o grupo "Administrador" se não existir
    admin_group, created = Group.objects.get_or_create(name='Administrador')
    
    if created:
        # Adiciona todas as permissões ao grupo "Administrador"
        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)