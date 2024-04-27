from django.shortcuts import render
from .forms import FileForm
import requests

API = 'http://localhost:5000'

# Create your views here.
def index(request):
    return render(request, 'index.html')

def transac(request):
    return render(request, 'transac.html')

def cargarXML(request):
    context = {
        'content': None
    }

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            txt = form.cleaned_data['file'].read()

            response = requests.post(API+'/postCargarConfig', data=txt)  # Agregar esta línea para depurar
            if response.status_code == 200:
                context['content'] = "El archivo se cargó correctamente."
            else:
                context['content'] = "Hubo un error al cargar el archivo. Por favor, inténtalo de nuevo."
        
        return render(request, 'respuesta.html', context)

    return render(request, 'respuesta.html', context)

def cargaTransac(request):
    context = {
        'content': None
    }

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            txt = form.cleaned_data['file'].read()

            response = requests.post(API+'/postCargarTransac', data=txt)  # Agregar esta línea para depurar
            if response.status_code == 200:
                context['content'] = "El archivo se cargó correctamente."
            else:
                context['content'] = "Hubo un error al cargar el archivo. Por favor, inténtalo de nuevo."
        
        return render(request, 'respuesta.html', context)

    return render(request, 'respuesta.html', context)

def inicializar(request):
    context = {
        'content': None
    }

    if request.method == 'POST':
        # Realizar la petición POST a la API para inicializar
        response = requests.delete(API + '/postInicializar')

        if response.status_code == 200:
            # Si la petición fue exitosa, establecer el mensaje de éxito en el contexto
            context['content'] = "Datos inicializados correctamente."
        else:
            # Si ocurrió algún error en la petición, establecer un mensaje de error en el contexto
            context['content'] = "Hubo un error al intentar inicializar los datos. Por favor, inténtalo de nuevo."

    # Renderizar el template con el contexto correspondiente
    return render(request, 'inicializar.html', context)