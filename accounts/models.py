from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from rest_framework.validators import UniqueValidator
from sectors.models import sectors
from simple_history.models import HistoricalRecords

class UserManager(BaseUserManager):
    """define um gerenciador de user personalizado que não vai usar username"""

    def _create_user(self, email, password, **extra_fields):
        """cria um usuário pedindo email e senha"""
        if not email:
            raise ValueError('Você precisa inserir um email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Cria e salva um user normal pedindo email e senha"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Cria e salva um superUser pedindo email e senha"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Um super user precisa do campo is_staff = true')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Um super user precisa do campo is_superuser = true')

        return self._create_user(email, password, **extra_fields)

#Modelo para a tabela de cargos
class office(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True, verbose_name= "Cargo")
    description = models.TextField(verbose_name="Descrição do cargo", blank=True, null=True, max_length=1000)
    created_at = models.DateTimeField(auto_now_add= True, verbose_name="Data de criação do cargo")
    updated_at = models.DateTimeField(auto_now= True, verbose_name="Última edição")
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    is_admin = models.BooleanField(default = False, null=True, blank=True)
    office = models.ForeignKey(office, max_length=255, verbose_name="Cargo", blank=False, null=False, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='users/profileImage/{self.email}/',blank=True, null=True)
    history = HistoricalRecords()
    
    # notice the absence of a "Password field", that is built in.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
    
    def __str__(self):
        return self.email
    
    objects = UserManager()