from django.shortcuts import redirect
from .models import Author

def author_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not Author.objects.filter(user=request.user).exists():
            return redirect('Crear_autor')
        return view_func(request, *args, **kwargs)
    return wrapper