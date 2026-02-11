from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def validar(request):
    responseData = {
        'id' : 4,
        'name' : 'Bryan',
        'roles' : ['Programador', 'Analista', 'Usuario']
    }

    return JsonResponse(responseData)