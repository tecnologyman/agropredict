from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Crea un superusuario automáticamente si no existe"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "treering")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "treering@tecnologyman.cl")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "treering123")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superusuario {username} creado"))
        else:
            self.stdout.write(self.style.WARNING(f"Superusuario {username} ya existe"))
