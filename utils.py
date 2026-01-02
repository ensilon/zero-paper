#!/usr/bin/env python3

import requests
from icmplib import ping


class Ping:
    def __init__(self, host="8.8.8.8"):
        self.host = host
        
    def rtt(self):
        stats = ping("8.8.8.8", privileged=False)
        rtt = int(stats.avg_rtt)
        return rtt


class Weather:
    def __init__(self, lat="43.451291", lon="-80.4927815"):
        owm_apikey = "c236ac822c68d3cfc4b4dc11ac5b3a8c"
        self.url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={owm_apikey}&units=metric"

    def forcast(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()
        except Exception as e:
            print(e)
            return {"ok": False}
        
        return {
            "ok": True,            
            "temperature":round(data['main']['temp']),
            "feels": round(data['main']['feels_like']),
            "description": data['weather'][0]['description'],
            "sunrise": data['sys']['sunrise'],
            "sunset": data['sys']['sunset'],
        }
