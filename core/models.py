from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.conf import settings


# Modelo de Usuario Personalizado

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    REQUIRED_FIELDS = ["phone_number"]

    class Meta:
        db_table = "users"
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.username} ({self.email})"
    
# class UserProfile(models.Model):
#     # El OneToOneField es la clave aquí.
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,  # Apunta a tu modelo User personalizado
#         on_delete=models.CASCADE,  # Si se borra un User, también se borra su UserProfile
#         related_name='profile')    # Opcional: Nombre para la relación inversa (ej. user.profile)
#         # Campos adicionales para el perfil (lo que me pediste agregar)
#     bio = models.TextField(verbose_name='Biografía', blank=True, null=True)
#     profile_picture = models.ImageField(
#             verbose_name='Foto de Perfil',
#             upload_to='my_app/profiles/pictures/', # Donde se guardarán las fotos
#             blank=True,
#             null=True
#         )
#     date_of_birth = models.DateField(verbose_name='Fecha de Nacimiento', blank=True, null=True)

#     class Meta:
#         db_table = "user_profiles"
#         verbose_name = 'Perfil de Usuario'
#         verbose_name_plural = 'Perfiles de Usuario'

#     def __str__(self):
#         return f"Perfil de {self.user.username}"

# Modelo de Club

class Club(models.Model):
    name = models.CharField(verbose_name='Nombre', unique=True, max_length=100)
    description = models.TextField(verbose_name='Descripción', max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    foundation_year = models.DateField(verbose_name="Año de Fundación", null=True, blank=True)
    titles_won = models.TextField(default=0, verbose_name="Títulos Ganados")
    coach_name = models.CharField(max_length=100, verbose_name="Nombre del Entrenador", null=True, blank=True)
    image = models.ImageField(
        verbose_name='Imagen',
        upload_to='Clubs/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        blank=True,
        null=True
    )

    class Meta:
        db_table = "clubs"
        verbose_name = 'Club'
        verbose_name_plural = 'Clubes'
    
    def __str__(self):
        return f"{self.name}"