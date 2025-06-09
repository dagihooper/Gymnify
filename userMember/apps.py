from django.apps import AppConfig


class UsermemberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userMember'
    
    def ready(self):
     import userMember.signals  
