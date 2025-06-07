from django.http import HttpResponse
from django.shortcuts import render
from joblib import load
from .models import Hostel
from sklearn.preprocessing import StandardScaler
import numpy as np 

#database import
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.hostelPricingDB
collectionD = db.SavedPredictions 


model = load("final_model")
scaler = load("scaler.joblib")

def home(request):
    return render(request,"index.html")

def calculate_price(request):

    lists = {
        'Tv': 'no', 'Air_conditioner': 'no', 'Refrigerator': 'no', 'Water_heater': 'no',
        'Modern_Wardrobe': 'no', 'Back_up_power_supply': 'no', 'Gym': 'no', 'Elevator': 'no',
        'Modernized_bathrooms': 'no', 'Room size': 0,
        'Location_Ayeduase': 'no', 'Location_Boadi': 'no', 'Location_Bomsu': 'no',
        'Location_Campus': 'no', 'Location_Kotei': 'no', 'Location_Newsite': 'no',
        'Location_Tech junction': 'no', 'Historical pricing data': 0
    }
    
    location= request.GET['location']
    lists['Room size']=int(request.GET['room_size'][0])
    lists['Historical pricing data']=float(request.GET['current_price'])

    #Removed number of people in a room from the training and test set
    # lists['Number of people in a room'] = float(request.GET['persons_per_room'])
    
    infrastructures = request.GET.getlist('infrastructure[]')
    appliances = request.GET.getlist('appliances[]')
    combined = infrastructures + appliances

    column_names = ['Tv', 'Air_conditioner', 'Refrigerator', 'Water_heater',
                   'Modern_Wardrobe', 'Back_up_power_supply', 'Gym', 'Elevator',
                   'Modernized_bathrooms']
    
    locations = ['Campus', 'Ayeduase', 'Kotei', 'Boadi', 'Tech junction', 'Newsite', 'Bomsu']

    for area in locations:
        if area == location:
            lists[f"Location_{area}"] = True
        else:
            lists[f"Location_{area}"] = False
    
    for name in column_names:
        if name in combined:
            lists[name] = True
        else:
            lists[name] = False
    

    input_data = [
        lists['Tv'], lists['Air_conditioner'], lists['Refrigerator'], lists['Water_heater'],
        lists['Modern_Wardrobe'], lists['Back_up_power_supply'], lists['Gym'], lists['Elevator'],
        lists['Modernized_bathrooms'], lists['Room size'],
        lists['Location_Ayeduase'], lists['Location_Boadi'], lists['Location_Bomsu'],
        lists['Location_Campus'], lists['Location_Kotei'], lists['Location_Newsite'],
        lists['Location_Tech junction'], lists['Historical pricing data']
    ]

    input_data = np.array(input_data).reshape(1, -1)

    input_data_scaled = scaler.transform(input_data)

    prediction = model.predict(input_data_scaled)

    prediction = round(float(prediction),2)

    # print(input_data_scaled)


    # response_text = f"Received data: {lists}"

    context = {'lists':lists,'prediction':prediction, 'form_data':request.GET}

    # print(lists)

    return render(request,"index.html",context)

def ViewAbout(request):
    return render(request, "about.html")

def ViewHelp(request):
    return render(request, "help.html")


def viewDatabase(request):
    hostels = list(collectionD.find({}))  
    context = {'hostels': hostels}  
    return render(request, "viewDB.html", context)


def updateDatabase(request):
    table= {}
    table['location']= request.POST.get('location')  
    table['RoomSize'] = request.POST.get('room_size') 
    infrastructure_list = request.POST.getlist('infrastructure[]')
    infrastructure_list = [item.replace('_',' ') for item in infrastructure_list]
    table['infrastructure'] = ', '.join(infrastructure_list)
    appliances_list = request.POST.getlist('appliances[]')
    appliances_list = [item.replace('_', ' ') for item in appliances_list]
    table['appliances']= ', '.join(appliances_list)
    table['Historical_Price'] = float(request.POST.get('current_price'))
    table['Current_Price'] = float(request.POST.get('prediction'))

    collectionD.insert_one(table)

    hostels = list(collectionD.find({}))  
    context = {'hostels': hostels}  
    return render(request, "viewDB.html", context)

def recommend_hostels(request):
    if request.method == 'GET':
        price = float(request.GET.get('prediction', 0))
        appliances = request.GET.getlist('appliances[]')
        infrastructure = request.GET.getlist('infrastructure[]')

        min_price = price - 150
        max_price = price + 150

        
        recommended_hostels = Hostel.objects.filter(
            price__gte=min_price,
            price__lte=max_price
        )

       
        def matches_features(hostel):
            return all(item in hostel.appliances for item in appliances) and \
                   all(item in hostel.infrastructure for item in infrastructure) 

        recommended_hostels = [hostel for hostel in recommended_hostels if matches_features(hostel)]

        context = {'recommended_hostels': recommended_hostels}
        return render(request, 'recommendations.html', context)