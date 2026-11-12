from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator

class EmailUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('El correo es obligatorio.')
        return super()._create_user(username, email.strip().lower(), password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField('Correo', unique=True)
    telefono = models.CharField('Telefono', max_length=15, blank=True,
        validators=[RegexValidator(r'^\+?[0-9]{10,14}$', 'Escribe de 10 a 14 digitos, con + opcional.')])
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = EmailUserManager()

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)
