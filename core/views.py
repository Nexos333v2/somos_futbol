from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
from .models import *
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm  
from .forms import RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

User = get_user_model()

def index(request):
    return render (request, 'index.html' )

def credits(request):
    return render (request, 'htmlPages/credits.html' )

def equipos(request):
    return render (request, 'htmlPages/equipos.html' )

def historia(request):
    return render (request, 'htmlPages/historia.html' )

def jugadores(request):
    return render (request, 'htmlPages/jugadores.html' )

def posiciones(request):
    return render (request, 'htmlPages/posiciones.html' )

def reglas(request):
    return render (request, 'htmlPages/reglas.html' )

def terminos(request):
    return render (request, 'htmlPages/terminos.html' )
    
def club_create(request):
    return render(request, 'CRUD/club_create.html')

def club_search(request):
    return render(request, 'CRUD/club_search.html')

def club_update(request, id):
    return render(request, 'CRUD/club_update.html')

def club_delete(request, id):
    return render(request, 'CRUD/club_delete.html')  

def club_read(request, id):
    return render(request, 'CRUD/club_read.html')

def equipos(request):
    clubs = Club.objects.all()
    return render(request, 'htmlPages/equipos.html', {'clubs': clubs})


class UserLoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        form = LoginForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('index') 
                else:
                    return render(request, self.template_name,
                                {'form': form,
                                'error_message': 'Nombre de usuario o contraseña incorrectos.'})

            return render(request, self.template_name, {'form': form})

class UserRegisterView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        form = RegisterForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, password=password)

            login(request, user)

            return redirect('equipos') # Cambia esto a tu página de inicio o dashboard

        return render(request, self.template_name, {'form': form})

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        # Cierra la sesión del usuario
        logout(request)
        # Redirige a la página de login o a la página de inicio
        return redirect('login')

class ClubCreateView(LoginRequiredMixin, View):
    template_name = 'CRUD/club_create.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        description = request.POST.get('description')
        city = request.POST.get('city')
        foundation_year = request.POST.get('foundation_year')
        titles_won = request.POST.get('titles_won')
        coach_name = request.POST.get('coach_name')
        image = request.FILES.get('image')

        errors = {}
        if not name:
            errors['name'] = "El nombre es obligatorio"
        if not city:
            errors['city'] = "La ciudad es obligatoria"
        if not foundation_year:
            errors['foundation_year'] = "El año de fundación es obligatorio"

        if errors:
            return render(request, self.template_name, {
                'errors': errors,
                'name': name,
                'description': description,
                'city': city,
                'foundation_year': foundation_year,
                'titles_won': titles_won,
                'coach_name': coach_name,
            })

        Club.objects.create(
            name=name,
            description=description,
            city=city,
            foundation_year=foundation_year,
            titles_won=titles_won if titles_won else 0,
            coach_name=coach_name,
            image=image
        )
        return redirect('equipos')  # Asegúrate de tener esta URL definida
    
class ClubUpdateView(LoginRequiredMixin, View):
    template_name = 'CRUD/club_update.html'

    def get(self, request, id, *args, **kwargs):
        club = get_object_or_404(Club, id=id)
        return render(request, self.template_name, {'club': club})

    def post(self, request, id, *args, **kwargs):
        club = get_object_or_404(Club, id=id)
        name = request.POST.get('name')
        description = request.POST.get('description')
        city = request.POST.get('city')
        foundation_year = request.POST.get('foundation_year')
        titles_won = request.POST.get('titles_won')
        coach_name = request.POST.get('coach_name')
        image = request.FILES.get('image')

        errors = {}
        if not name:
            errors['name'] = "El nombre es obligatorio"
        if not city:
            errors['city'] = "La ciudad es obligatoria"
        if not foundation_year:
            errors['foundation_year'] = "El año de fundación es obligatorio"

        if errors:
            return render(request, self.template_name, {
                'errors': errors,
                'club': club,
                'name': name,
                'description': description,
                'city': city,
                'foundation_year': foundation_year,
                'titles_won': titles_won,
                'coach_name': coach_name,
            })

        club.name = name
        club.description = description
        club.city = city
        club.foundation_year = foundation_year
        club.titles_won = titles_won if titles_won else 0
        club.coach_name = coach_name
        if image:
            club.image = image
        club.save()
        return redirect('equipos')

    
class ClubDeleteView(LoginRequiredMixin, View):
    template_name = 'CRUD/club_delete.html'

    def get(self, request, id, *args, **kwargs):
        club = get_object_or_404(Club, id=id)
        return render(request, self.template_name, {'club': club})

    def post(self, request, id, *args, **kwargs):
        club = get_object_or_404(Club, id=id)
        club.delete()
        return redirect('equipos')
    
    
class ClubListView(View):
    template_name = 'CRUD/club_search.html'
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        clubs = Club.objects.all()
        query = request.GET.get('q')

        if query:
            clubs = clubs.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()

        paginator = Paginator(clubs, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'clubs': page_obj.object_list
        }

        return render(request, self.template_name, context)