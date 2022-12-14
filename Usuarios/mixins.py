import requests
from django.conf import settings
from humanfriendly import format_timespan
from django.shortcuts import redirect
'''
Handles directions from Google
'''
def Directions(*args, **kwargs):
    lat_a = kwargs.get("lat_a")
    long_a = kwargs.get("long_a")
    lat_b = kwargs.get("lat_b")
    long_b = kwargs.get("long_b")
    lat_c = kwargs.get("lat_c")
    long_c = kwargs.get("long_c")
    lat_d = kwargs.get("lat_d")
    long_d = kwargs.get("long_d")
    lat_e = kwargs.get("lat_e")
    long_e = kwargs.get("long_e")
    lat_f = kwargs.get("lat_f")
    long_f = kwargs.get("long_f")
    lat_g = kwargs.get("lat_g")
    long_g = kwargs.get("long_g")
    lat_h = kwargs.get("lat_h")
    long_h = kwargs.get("long_h")
    lat_i = kwargs.get("lat_i")
    long_i = kwargs.get("long_i")
    lat_j = kwargs.get("lat_j")
    long_j = kwargs.get("long_j")
    lat_k =  kwargs.get("lat_k")
    long_k = kwargs.get("long_k")

    origin = f'{lat_a},{long_a}'
    destination = f'{lat_b},{long_b}'
    waypoints = f'{lat_c},{long_c}|{lat_d},{long_d}|{lat_e},{long_e}|{lat_f},{long_f}|{lat_g},{long_g}|{lat_h},{long_h}|{lat_i},{long_i}|{lat_j},{long_j}|{lat_k},{long_k}'
    result = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?',
         params={
         'origin': origin,
         'destination': destination,
         'waypoints': waypoints,
         "key": settings.API_KEY
         })
    directions = result.json()
    distance = 0
    duration = 0
    print(directions["status"])
    if directions["status"] == "OK":
        routes = directions["routes"][0]["legs"]
        distance = 0
        duration = 0
        route_list = []
        for route in range(len(routes)):
            distance += int(routes[route]["distance"]["value"])
            duration += int(routes[route]["duration"]["value"])
            route_step = {
                'origin': routes[route]["start_address"],
                'destination': routes[route]["end_address"],
                'distance': routes[route]["distance"]["text"],
                'duration': routes[route]["duration"]["text"],
                'steps': [
                    [
                        s["distance"]["text"],
                        s["duration"]["text"],
                        s["html_instructions"],
                    ]
                    for s in routes[route]["steps"]]
                }
            route_list.append(route_step)
    else:
        print(directions["status"])
        print("Error entre al else dentro de else de los mixins")

    return {
        "origin": origin,
        "destination": destination,
        "distance": f"{round(distance/1000, 2)} Km",
        "duration": format_timespan(duration),
        "route": route_list
        }

def if_admin(request):
    if request.user.administrador:
        return True
    else:
        return False

  
           