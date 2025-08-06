from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext_lazy as _



class Cantor(models.Model):
    musica = models.CharField(max_length=200)
    esperando = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} - {self.musica}"


class Banner(models.Model):
    titulo = models.CharField(max_length=200, blank=True, null=True)
    imagem = models.ImageField(upload_to='banners/')
    

    def __str__(self):
        return self.titulo or f"Banner {self.id}"
    
class Promocao(models.Model):
    titulo = models.CharField(max_length=200, blank=True, null=True)  # nome da promoção
    imagem = models.ImageField(upload_to='promocoes/')               # foto do combo ou promoção
    descricao = models.TextField(blank=True, null=True)              # texto explicativo da promoção
    valor = models.DecimalField(max_digits=8, decimal_places=2)      # valor do combo ou promoção

    def __str__(self):
        return self.titulo or f"Promoção {self.id}"
    
class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, email, first_name, last_name, password=None, **extra_fields):
        if not cpf:
            raise ValueError('O CPF é obrigatório')
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(
            cpf=cpf,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(cpf, email, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.cpf})"