from django.contrib import admin
from django.urls import path, include
from fila_karaoke import views
from django.contrib.auth import views as auth_views
from fila_karaoke.views import CustomLoginView


urlpatterns = [
    path('', views.fila_karaoke, name='fila_karaoke'),
    path('adicionar/', views.adicionar_cantor, name='adicionar_cantor'),
    path('cantou/<int:cantor_id>/', views.cantou, name='cantou'),
    path('promocoes/', views.promocoes, name='promocoes'),


    # Em vez de "admin", use "painel" para evitar conflitos:
    path('painel/promocao/editar/<int:pk>/', views.editar_promocao, name='editar_promocao'),
    path('painel/promocao/excluir/<int:pk>/', views.excluir_promocao, name='excluir_promocao'),
    path('painel/usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('painel/', views.painel_admin, name='painel_admin'),
    path('painel/promocao/nova/', views.criar_promocao, name='criar_promocao'),


    path('tv/', views.tv_player, name='tv_player'),

    # Login, logout e registro
   
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
