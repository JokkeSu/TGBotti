try:
    import requests
except ImportError:
    requests = None
    print("Could not import module 'requests'")

class WeatherInfo:
    api_url = ""