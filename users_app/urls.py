from django.contrib import admin
from django.urls import path
from users_app.views import *
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
from . import views



urlpatterns = [

# NAVBAR
    path ("home", home, name="Inicio"),
    path ("blog/", blog, name="Articulos"),
    path ("post/", post, name="Leer mas"),
    path ("team/", team, name="Nosotros"),
    path ("contact/", Contact_view.as_view(), name="Contacto"),
    path("recent_posts/", get_recent_posts.as_view(), name="Publicaciones_recientes"),




# BLOG - POST

  # Versión inicial
    # path("create_new_post/", create_new_post, name="Nuevo_post"),
    # path("post_new_post/", post_new_post, name="Publicar"),
    path( "search_post/", search_post, name="Buscar_post"),
    path( "found_post/", found_post, name="Resultado_post"),

  #Vistas basadas en clases
    path( "list_post/", Post_list.as_view(), name="Lista_post"),   #aca ya no ponemos una función sino la vista invocando el método asview para que opere precisamnete como una función. 
    path( "post_detail/<pk>/", Post_detail.as_view(), name="Leer_publicacion"),  #tenemos que agregar el atributo que queremos, para que le permita a la vista identificar el registro concreto 
    path( "post_create/",Post_create.as_view(), name="Crear_publicacion"), 
    path( "post_update/<pk>/",Post_update.as_view(), name="Editar_publicacion"),
    path( "post_delete/<pk>/",Post_delete.as_view(), name="Eliminar_publicacion"),
    path( "confirm_post_delete/<pk>/",Post_delete.as_view(), name="Confirma_eliminacion"),
    path('blog/post/<int:pk>/', Post_detail.as_view(), name='Leer mas'), 



#AUTORES

  # Versión inicial
    # path ("autor/", author, name="Autores"),
    # path("create_new_author/", create_new_author, name="Nuevo_autor"),
    # path ("published_post/", author_list, name="Lista_de_autores"),
    # path ("author_list/", author_list, name="Lista_de_autores"),
    # path ("register/", new_author),
    # path ("publicacionesporautor/", get_publications),
    path( "search_author", search_author, name="Buscar_autor"),
    path( "found_author", found_author, name="Resultado_autor"),

  #Vistas basadas en clases
    path( "list_authors/", Author_list.as_view(), name="Lista_autores"), 
    path( "author_create/",Author_create.as_view(), name="Crear_autor"), 
    path( "author_update/<pk>/",Author_update.as_view(), name="Editar_autor"),
    path( "author_delete/<pk>/",Author_delete.as_view(), name="Eliminar_autor"),
    path( "confirm_author_delete/<pk>/",Author_delete.as_view(), name="Confirma_eliminacion_autor"), 




# USERS
    path( "login/", login_view, name="Login"),
    path( "signup/", signup_view, name="Registro"),
    path( "logout/", LogoutView.as_view(template_name="logout.html"), name="Cerrar_sesión"),   #vista basada en clase pide template de parametro para renderizar.
    path( "update_user/", update_user, name="Actualizar_perfil"),
    path("create_avatar/<pk>/", Avatar_create.as_view(), name="foto_de_perfil"),
    path("upload_avatar/", views.upload_avatar, name="Subir_foto_perfil"),

# CONTACT

path ("send_message/", send_message, name="Mensaje_enviado"),



]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)