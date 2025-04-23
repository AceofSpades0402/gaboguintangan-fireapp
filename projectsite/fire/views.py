from django.shortcuts import render
from django.views.generic.list import ListView
from fire.models import Locations, Incident, FireStation


class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super(). get_context_data(**kwargs)
        return context
    
    def get_queryset(self, *args, **kwargs):
        pass


def map_station(request):
    fireStations = FireStation.objects.values('name', 'latitude', 'longitude')

    for fs in fireStations:
        fs['latitude'] = float(fs['latitude'])
        fs['longitude'] = float(fs['longitude'])

    fireStations_list = list(fireStations)

    context = {
        'fireStations': fireStations_list,
    }

    return render(request, 'map_station.html', context)



def map_incidents(request):
    fireIncidents = Incident.objects.select_related('location').values(
        'description',
        'location__latitude',
        'location__longitude',
        'date_time'
    )

    fireIncidents_list = []
    for incident in fireIncidents:
        fireIncidents_list.append({
            'description': incident['description'],
            'latitude': float(incident['location__latitude']),
            'longitude': float(incident['location__longitude']),
            'date': incident['date_time'].strftime('%Y-%m-%d') if incident['date_time'] else '',
        })

    context = {
        'fireIncidents': fireIncidents_list,
    }

    return render(request, 'map_incidents.html', context)

