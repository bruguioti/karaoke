from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Cantor, Banner, Promocao
from django.utils.timezone import now
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Cantor, Promocao, CustomUser
from .forms import PromocaoForm  # vamos criar isso já já
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch

@staff_member_required
def painel_admin(request):
    cantores = Cantor.objects.filter(esperando=True).order_by('criado_em')
    promocoes = Promocao.objects.all()
    total_cantores = Cantor.objects.count()
    return render(request, 'painel_admin.html', {
        'cantores': cantores,
        'promocoes': promocoes,
        'total_cantores': total_cantores,
    })

@staff_member_required
def editar_promocao(request, pk):
    promocao = get_object_or_404(Promocao, pk=pk)
    if request.method == 'POST':
        form = PromocaoForm(request.POST, request.FILES, instance=promocao)
        if form.is_valid():
            form.save()
            return redirect('painel_admin')
    else:
        form = PromocaoForm(instance=promocao)
    return render(request, 'editar_promocao.html', {'form': form})

@staff_member_required
def excluir_promocao(request, pk):
    promocao = get_object_or_404(Promocao, pk=pk)
    if request.method == 'POST':
        promocao.delete()
        return redirect('painel_admin')
    return render(request, 'confirmar_exclusao.html', {'obj': promocao})

@staff_member_required
def lista_usuarios(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})

@staff_member_required
def criar_promocao(request):
    if request.method == 'POST':
        form = PromocaoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('painel_admin')
    else:
        form = PromocaoForm()
    return render(request, 'criar_promocao.html', {'form': form})

@login_required
def fila_karaoke(request):
    cantores = Cantor.objects.filter(esperando=True).order_by('criado_em')
    hoje = now().date()
    musicas_cantadas_hoje = Cantor.objects.filter(esperando=False, criado_em__date=hoje).count()
    banners = Banner.objects.all()
    promocoes = Promocao.objects.all()  # NOVO

    return render(request, 'fila_karaoke.html', {
        'cantores': cantores,
        'musicas_cantadas_hoje': musicas_cantadas_hoje,
        'banners': banners,
        'promocoes': promocoes,  # NOVO
    })


@login_required
def adicionar_cantor(request):
    if request.method == 'POST':
        musica = request.POST.get('musica', '').strip()
        if musica:
            Cantor.objects.create(musica=musica, usuario=request.user)
    return redirect('fila_karaoke')




def tv_player(request):
    cantor_atual = Cantor.objects.filter(esperando=True).order_by('criado_em').first()
    video_id = None

    if cantor_atual:
        # Monta a query com o nome da música e "karaoke"
        search_query = f"{cantor_atual.musica} karaoke"

        # Faz busca com youtube-search-python
        videos_search = VideosSearch(search_query, limit=1)
        results = videos_search.result()

        if results.get('result'):
            video_url = results['result'][0]['link']  # exemplo: https://www.youtube.com/watch?v=abc123
            if 'v=' in video_url:
                video_id = video_url.split('v=')[1]

    return render(request, 'tv_player.html', {
        'cantor': cantor_atual,
        'video_id': video_id
    })


@login_required
def cantou(request, cantor_id):
    cantor = Cantor.objects.filter(pk=cantor_id, usuario=request.user, esperando=True).first()
    if cantor:
        cantor.esperando = False
        cantor.save()
    else:
        # opcional: mensagem ou tratamento caso não tenha permissão
        pass
    return redirect('fila_karaoke')



def home(request):
    banners = Banner.objects.all()
    return render(request, 'home.html', {'banners': banners})

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'


def login_manual(request):
    form = AuthenticationForm()
    return render(request, 'fila_karaoke/registration/login.html', {'form': form})

def promocoes(request):
    promocoes = Promocao.objects.all()
    return render(request, 'promocoes.html', {'promocoes': promocoes})
