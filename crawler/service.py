import requests


def get_my_ip():
    result = requests.get('https://api.ipify.org?format=json')
    return result.json()
