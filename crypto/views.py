from rest_framework.decorators import api_view
from django.http import JsonResponse
import urllib.request
from bs4 import BeautifulSoup
import urllib.error

def get_price():
    url= 'https://cointelegraph.com/bitcoin-price-index'
    page= urllib.request.urlopen(url)
    pars= BeautifulSoup(page,'html.parser')
    price= pars.find('span',attrs={'class':'price-value'}) #the html tag was div before, but now it's span

    return price.text.strip()

@api_view(["POST", "GET"])
def index(request):
    if(request.method == 'POST'):
        return JsonResponse(data={"status": 200, "Price": get_price()})
    else:
        return JsonResponse(data={"status": 200, "Price": get_price()})
