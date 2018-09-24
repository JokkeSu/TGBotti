try:
    import requests
except ImportError:
    requests = None
    print("Could not import module 'requests'")

class WeatherInfo():
    #TODO: Get api-key from heroku config
    api_url = "http://data.fmi.fi/fmi-apikey/{}/wfs?request=getCapabilities".format(api_key)

    def getInfo(self):
        print("TODO: getInfo from {}".format(self.api_url))
        resp = requests.get(self.api_url)

        print(resp.content)



def main():
    wi = WeatherInfo()

    wi.getInfo()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
