from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from .forms import *
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .decorators import *
from django.db import IntegrityError

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.contrib import messages





# Create your views here.



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NAV-BAR
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def home(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).first()
        avatar_url = avatar.imagen.url if avatar else None
        return render(request, "home.html", {"avatar_url": avatar_url})
    except:
        return render(request, "home.html")


        
def author(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).first()
        avatar_url = avatar.imagen.url if avatar else None
        return render(request, "author.html", {"avatar_url": avatar_url})
    except:
        return render(request, "author.html")


def blog(request):
    posts = Post.objects.all()
    try:
        avatar = Avatar.objects.filter(user=request.user.id).first()
        avatar_url = avatar.imagen.url if avatar else None
        return render(request, "blog.html", {"posts": posts, "avatar_url": avatar_url})
    except:
        return render(request, "blog.html", {"posts": posts})


def post(request):
    return render(request, "post_detail.html")


def new_post(request):
    return render(request, "new_post.html")


def authors(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).first()
        avatar_url = avatar.imagen.url if avatar else None
        return render(request, "author.html", {"avatar_url": avatar_url})
    except:
        return render(request, "author.html")


def team(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).first()
        avatar_url = avatar.imagen.url if avatar else None
        return render(request, "team.html", {"avatar_url": avatar_url})
    except:
        return render(request, "team.html")


def contact(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).first()
        avatar_url = avatar.imagen.url if avatar else None
        return render(request, "contact.html", {"avatar_url": avatar_url})
    except:
        return render(request, "contact.html")




# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BLOG-POST
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# def create_new_post (request):
#     print ("method: ", request.method)
#     print ("post: ", request.POST)

#     if request.method == "POST":
        
#         new_post_form = Form_new_post(request.POST)
          
#         print(new_post_form)

#         if new_post_form.is_valid():
             
#           data = new_post_form.cleaned_data
   
#           post = Post(author=data["author"],title=data["title"], content=data["content"], category=data["category"], tags=data["tags"])
#           post.save()
        
#           return render (request, "published_post.html") 
        
#         else:
#              return render (request, "published_post.html", {"Mensaje": "Formulario inválido"}) 
    
#     else:    
#         new_post_form = Form_new_post()

#         return render (request, "create_new_post.html", {"new_post_form": new_post_form})
    

def search_post(request):
    
    return render (request, "search_post.html")

def found_post(request):
    if request.GET["title"]:
        title = request.GET["title"]
        posteos = Post.objects.filter(title__icontains=title)
        return render(request, "found_post.html", {"title": title, "posteos": posteos})
    else:
        
      return HttpResponse(f'No enviaste info')


# def post_new_post (request):
#     print ("method: ", request.method)
#     print ("post: ", request.POST)
#     return render (request, "published_post.html")



# def published_post (request):
#   return render (request, "published_post.html")

# def delete_post (request, id):
     
#      if request.method =="POST":
          
#           post = Post.objects.get(id=id)   #el ID de la izq es el de la BD
#           post.delete ()    

#           post = Post.objects.all()
#           return render (request, "post_delete.html", {"post": post})
     


class Post_list(ListView):
    model = Post     # le tengo que definri el modelo con el cual va a operar, a gobernar esta vista. 
    template_name= "list_post.html"     #definir el HTML que va a renderizar este listado. 
    context_object_name = "posts"   # Accedo directamente el listado de cursos sin usar el manager. Para eso uso como variable de contexto esta variable. Dentro de "posts" estará el listado de post. 

  

class get_recent_posts(ListView):
    model = Post
    template_name = "recent_post.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.order_by('-pub_date')[:3]


class Post_detail(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post_detail_view"
    
 #En este caso debemos definir: 1) que campos queremos que se vizualicen al mostrar el form, y 2) donde quiero que me dirija al enviar los datos.


class Post_create(LoginRequiredMixin, CreateView):
    model = Post
    template_name ="create_post.html"
    fields = ("title", "content", "tags", "category", "author")
    success_url= reverse_lazy("Lista_post")
    labels = {
        'title': 'Título',
        'content': 'Contenido',
        'tags': 'Etiquetas',
        'category': 'Categoría',
        'author': 'Autor',
        
    }


class Post_update(UpdateView):
    model = Post
    template_name = "post_update.html"
    fields = "__all__"
    success_url= reverse_lazy("Lista_post")


class Post_delete(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url= reverse_lazy("Lista_post")


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AUTORES
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def author_list (self):
     return render (self, "author.html")

def get_publications(self):          #Función para listar todos los post realizados por una persona.
      post_list = Post.objects.all()  #Los managers son los que nos entregasn la URL de Django y conecta con la BD. Es el nexo con la BD
     
      return render (self, "post_list.html", {"post_list": post_list}) 

def get_authors (request):
     authors = Author.objects.all()
     return render (request, "get_authors.html", {"authors": authors})

def search_author(request):
    
    return render (request, "search_author.html")


def found_author(request):
    if request.GET["pseudonym"]:
        autor = request.GET["pseudonym"]
        autores = Author.objects.filter(pseudonym__icontains=autor)
        print(autores)
        return render(request, "found_author.html", {"autor": autor, "autores": autores})
    else:
        
      return HttpResponse(f'No enviaste info')


class Author_list(ListView):
    model = Author     # le tengo que definri el modelo con el cual va a operar, a gobernar esta vista. 
    template_name= "list_author.html"     #definir el HTML que va a renderizar este listado. 
    context_object_name = "list_authors"   # Accedo directamente el listado de autores sin usar el manager. Para eso uso como variable de contexto esta variable. Dentro de "authors" estará el listado de autores. 


class Author_create(LoginRequiredMixin, CreateView):
    model = Author
    template_name = "create_author.html"
    fields = ("expertise", "academic_titles", "pseudonym",)
    success_url = reverse_lazy("Lista_autores")
    labels = {
        'expertise': 'Especialización',
        'academic_titles': 'Profesión',
        'pseudonym': 'Alias',
  
    }

class Author_update(UpdateView):
    model = Author
    template_name = "author_update.html"
    fields = "__all__"
    success_url= reverse_lazy("Lista_autores")
    context_object_name = "authors"


class Author_delete(DeleteView):
    model = Author
    template_name = "author_delete.html"
    success_url= reverse_lazy("Lista_autores")





# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# USER
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def login_view (request):
    if request.method == "POST":
          
        login_form = AuthenticationForm(request, data=request.POST)

        if login_form.is_valid():
            data = login_form.cleaned_data
            user = data ["username"]
            psw = data ["password"]

            user = authenticate(username=user, password=psw)   #esta funcion devuelve un usuario o un none. Si el usuario existe devuelve eso, y sino el none. No arroja un error, sino que retorna none si falla.

            if user:  #si el usuario existe, procedemos a loguearlo. Abrimos sesión de ese usuario. En Django se hace con cookies. 
                login(request, user)
                return render (request, "home.html", {"hi_msj": f"Hola {user}"})   #diferencio el mensaje para poder ubicarlo en diferentes espacios. El hola en la nav y el error en el hero. Tb creo otro template
                                                                                    #para poder mostrar una interfaz diferenciada y cambiar el CTA a publicar en lugar de crear cuenta.  
            else:
                return render (request, "home.html", {"error_msj": f"Error: datos incorrectos"})


        else: 
            return render (request, "home.html", {"error_msj": "Formulario inválido"})

    else:
        login_form = AuthenticationForm()
        return render (request, "login.html", {"login_form": login_form})


def signup_view (request):

    if request.method == "POST":
        signup_form = UserCreationForm(request.POST)

        if signup_form.is_valid():
            data = signup_form.cleaned_data
            username = data ["username"]
            # signup_form.save()   #este metodo toma los valores de la request y realiza un proceso de encriptado de esa info y guardado en la base de datos. 
            user = signup_form.save()
            login(request, user)
            return render (request, "home.html", {"signup_msj": f"¡{username} creaste exitosamente tu perfil!."})
            
            
        else: 
            print(signup_form.errors)
            return render (request, "home.html", {"error_msj": "Formulario inválido"})

    else:
        signup_form = UserCreationForm()
        return render (request, "signup.html", {"signup_form": signup_form})
    


@login_required
def update_user(request):
    user_target = request.user

    if request.method == "POST":
        form_update_user = User_update_form(request.POST, instance=user_target)

        if form_update_user.is_valid():
            data = form_update_user.cleaned_data
            
            user_target.username = data["username"]
            user_target.email = data["email"]
            user_target.first_name = data["first_name"]
            user_target.last_name = data["last_name"]

            password1 = data["password1"]
            password2 = data["password2"]

            if password1 != password2:
                form_update_user.add_error('password2', 'Las contraseñas no coinciden.')
                return render(request, "update_user.html", {"form_update_user": form_update_user})

            user_target.set_password(password1)
            user_target.save()

            return render(request, "home.html")
        
        else: 
            return render(request, "update_user.html", {"form_update_user": form_update_user})
    else:
        form_update_user = User_update_form(instance=user_target)
        return render(request, "update_user.html", {"form_update_user": form_update_user})

        

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AVATAR
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Avatar_create(LoginRequiredMixin, CreateView):
    model = Avatar
    template_name = "create_avatar.html"
    form_class = Avatar_Create_Form
    success_url = reverse_lazy("Inicio")
    context_object_name = "Avatar"

    def form_valid(self, form):
        avatar = form.save(commit=False)
        avatar.user = self.request.user
        avatar.save()

        # Obtener la última imagen cargada del usuario actual
        latest_avatar = Avatar.objects.filter(user=self.request.user).latest('created_at')
        self.request.session['latest_avatar_id'] = latest_avatar.id

        return redirect(self.success_url)

    def form_invalid(self, form):
        context = {'form': form}
        return render(self.request, 'new_avatar.html', context)



@login_required
def upload_avatar(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        profile_pic = request.FILES.get('profile_pic')

        if profile_pic:
            if profile_pic.size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError('El archivo es demasiado grande (máximo %s bytes)' % settings.MAX_UPLOAD_SIZE)

            # Creamos una instancia de FileSystemStorage para la carpeta "avatares"
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'avatares'))
            filename = fs.save(profile_pic.name, profile_pic)
            
            # Creamos una instancia de Avatar y la asociamos con el usuario
            avatar = Avatar(user=user, imagen=os.path.join('avatares', filename))
            avatar.save()

        return redirect('Inicio')

    return render(request, 'upload_avatar.html')





# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTACT FORM
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Contact_view(FormView):
    template_name = 'contact.html'
    form_class = Contact_form
    success_url = reverse_lazy('Mensaje_enviado')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Tu mensaje fue enviado correctamente ¡Gracias!')
        return super().form_valid(form)
    


def send_message(request):
    
    return render(request, "contact_send.html")