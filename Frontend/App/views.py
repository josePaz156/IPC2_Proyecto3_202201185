from django.shortcuts import render
from .forms import FileForm
import requests

API = 'http://localhost:5000'

# Create your views here.
def index(request):
    return render(request, 'index.html')

def cargarXML(request):
    context = {
        'content': None
    }

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            txt = form.cleaned_data['file'].read()

            response = requests.post(API+'/postCargarConfig', data=txt)
            print("Contenido de la respuesta del servidor:", response.text)  # Agregar esta línea para depurar
            if response.status_code == 200:
                context['content'] = "El archivo se cargó correctamente."
            else:
                context['content'] = "Hubo un error al cargar el archivo. Por favor, inténtalo de nuevo."
        
        return render(request, 'respuesta.html', context)

    return render(request, 'carga.html', context)