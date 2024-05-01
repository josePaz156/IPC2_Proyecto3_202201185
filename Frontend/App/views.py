from django.shortcuts import render
from .forms import FileForm
from django.http import HttpResponse
import requests

API = 'http://localhost:5000'

# Create your views here.
def index(request):
    return render(request, 'index.html')

def grafico(request):
    return render(request, 'grafico.html')

def transac(request):
    return render(request, 'transac.html')

def peticiones(request):
    return render(request, 'peticiones.html')

def cargarXML(request):
    context = {
        'content': None
    }

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            txt = form.cleaned_data['file'].read()

            response = requests.post(API+'/postCargarConfig', data=txt)
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

            response = requests.post(API+'/postCargarTransac', data=txt)
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
        response = requests.delete(API + '/postInicializar')

        if response.status_code == 200:
            context['content'] = "Datos inicializados correctamente."
        else:
            context['content'] = "Hubo un error al intentar inicializar los datos. Por favor, inténtalo de nuevo."

    return render(request, 'inicializar.html', context)

def consultar_estado_cuenta(request):
    context = {}  # Inicializa un diccionario para el contexto

    if request.method == 'GET':
        nit = request.GET.get('NIT')  # Obtiene el NIT del formulario

        # Envía la solicitud al endpoint correcto del API Flask
        response = requests.get(f'{API}/getConsultarCuenta/{nit}')

        if response.status_code == 200:
            # Parsea la respuesta JSON y extrae el informe
            informe = response.json()
            context['informe'] = informe
        else:
            context['error'] = 'Error al consultar el estado de cuenta.'

    return render(request, 'peticiones.html', context)

def mostar_clientes(request):
    context = {}

    response = requests.get(API + '/getListadoClientes')
    if response.status_code == 200:
        listado = response.text
        context['listado'] = listado 
    else:
        context['error'] = 'Error.'

    return render(request, 'peticiones.html', context)

def generar_grafico(request):

    context = {}

    if request.method == 'GET':

        mes = request.GET.get('mes')
        año = request.GET.get('año')

        params = {'mes': mes, 'año': año}

        response = requests.get(API + '/graphs', params=params)

        bancos = []
        ganancias = []

        if response.status_code == 200:
            # Parsea la respuesta JSON y extrae el informe
            informe = response.json()
            
            print(informe)

            for banco in informe:
                bancos.append(banco)
                print(banco)

                ganancias.append(informe[banco])

                print(informe[banco])
            
            context = {
                'bancos': bancos,
                'ganancias': ganancias
            }

            return render(request, 'grafico.html', context)