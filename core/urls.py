from django.urls import path
from core.views import *
from . import views

urlpatterns = [
    path ('', index, name = 'index'),
    path ('credits/', credits, name = 'credits'),
    path ('equipos/', equipos, name = 'equipos'),
    path ('historia/', historia, name = 'historia'),
    path ('jugadores/', jugadores, name = 'jugadores'),
    path ('posiciones/', posiciones, name = 'posiciones'),
    path ('reglas/', reglas, name = 'reglas'),
    path ('terminos/', reglas, name = 'terminos'),
    
    path('clubs/create/', views.ClubCreateView.as_view(), name='club_create'),
    path('clubs/search/', views.ClubListView.as_view(), name='club_search'),
    path('clubs/update/<int:id>/', views.ClubUpdateView.as_view(), name='club_update'),
    path('clubs/delete/<int:id>/', views.ClubDeleteView.as_view(), name='club_delete'),
    path('clubs/read/<int:id>/', views.club_read, name='club_read'),
    
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]