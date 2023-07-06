from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from config.settings import MEDIA_URL, STATIC_URL,DEFAULT_AZURE_PATH
# practicamente voy a modificar la creacion para super usuario y usuarios
class MyAccountManager(BaseUserManager):
    # con esto creo el usuario normal, y los pido con esos valores
    def create_user(self,first_name,last_name,email,username,password=None):
        # lanzo errro si no me pasa un email o username
        if not email:
            raise ValueError('El usuario debe tener un email')
        if not username:
            raise ValueError('El usuario debe tener un username')
        
        user=self.model( # con el model creo el usuario
            email=self.normalize_email(email), # le aplico la normalizacion al email
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password) # le paso la contraseña, practicamenta la encripto
        user.save(using=self._db) # lo guardo y le paso el using
        return user
    
    def create_superuser(self,first_name,last_name,email,username,password=None): # lo mismo pero le pongo el true los valores para que sea super usuario
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
# Create your models here.

class Account(AbstractBaseUser): #para crear los campos de los usuarios, en este caso le aumente el del telefono
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # campos atributos de django - atributos por defectp de django que debo crearle si utilizo AbstractBaseUser
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD='email' #para que no utilice el username para inicio sino el email

    REQUIRED_FIELDS=['username', 'first_name', 'last_name' ]# para que en el formulario muestre estos como requeridos

    objects=MyAccountManager() # para que pueda utilizar las funciones de crear usuarios y super usuarios

    def full_name(self):
        return self.first_name+" "+self.last_name

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None): # si es admin tiene algunos permisos
        return self.is_admin

    def has_module_perms(self,perm,obj=None): # si es admin tiene algunos permisos
        return self.is_admin

class UserProfile(models.Model):
    user=models.OneToOneField(Account,on_delete=models.CASCADE)
    address_line_1=models.CharField(max_length=100,blank=True)
    address_line_2=models.CharField(max_length=100,blank=True)
    profile_picture=models.ImageField(blank=True,upload_to=f'{MEDIA_URL}/userprofile')
    city=models.CharField(max_length=20,blank=True)
    state=models.CharField(max_length=20,blank=True)
    country=models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        return DEFAULT_AZURE_PATH+STATIC_URL+'media/img/avatars/picture-user-empty.png'
    