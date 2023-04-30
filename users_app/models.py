from django.db import models

from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from builtins import property

from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.



class Author(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_profiles')
    num_followers = models.IntegerField(default=0,)
    expertise = models.CharField(max_length=100, blank=True, null=True, verbose_name="Especialización")
    academic_titles = models.CharField(max_length=100, blank=True, null=True, verbose_name="Profesión")
    pseudonym = models.CharField(max_length=100, null=True, verbose_name="Alias")
    # author_username = models.CharField(max_length=30, unique=True) # Cambiar el nombre del campo 'username' a 'author_username' con unique=True


    def __str__(self):
        return self.pseudonym
    
    def __str__(self):
        return self.pseudonym


    class Meta:   #nos permite modificar el comportamiento de la clase en el admin
      verbose_name= "Autor"
      verbose_name_plural = "Autores"
      ordering = ("pseudonym",)  #recibe una tupla
      unique_together = ["pseudonym",]   #puede recibir lista o tupla


     
class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título")
    content = models.TextField(verbose_name="Contenido")
    pub_date = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Fecha de Publicación")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Autor")
    tags = models.CharField(default=None, max_length=200, blank=True, verbose_name="Etiquetas")
    category = models.CharField(default="Actualidad", max_length=50, blank=True, verbose_name="Categoría")
    

    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    @property
    def formatted_pub_date(self):
        return self.pub_date.strftime("%d/%m/%Y")
  
    class Meta:
        verbose_name= "Articulo"
        



class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.imagen.url}"
    
    def get_avatar_url(self):
        if self.imagen:
            return self.imagen.url
        else:
            # En caso de que no haya imagen definida para el avatar, se puede retornar una imagen predeterminada
            return '/static/assets/img/graduated.png'


class Best_seller_author(Author):
    best_seller_ranking = models.IntegerField()
