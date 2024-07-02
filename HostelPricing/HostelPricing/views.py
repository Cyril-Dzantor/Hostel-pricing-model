from django.http import HttpResponse
from django.shortcuts import render
from joblib import load


def home(request):
    return render(request,"index.html")

def calculate_price(request):
    model = load("final_model.sav")
    lists = []
    lists.append(request.GET['location'])
    lists.append(request.GET['room_size'])
    infrastructures = request.GET.getlist('infrastructure')
    appliances = request.GET.getlist('appliances')

    lists.extend(infrastructures)
    lists.extend(appliances)

    print(lists)

    response_text = f"Received data: {lists}"

    return HttpResponse(response_text)