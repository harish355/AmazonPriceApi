from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
import re
from bs4 import BeautifulSoup

def get_headers():
    return {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
            "cache-control": "max-age=0",
            "dnt": "1",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}


@api_view(["POST", "GET"])
def index(request):
    if(request.method == 'POST'):
        try:
            data = request.data
            url = data['url']
        except:
            return JsonResponse(data={"status": 302, "message": "Invalid Parameter"})
        try:
            ip = request.META.get("REMOTE_ADDR")
            print(ip)
        except:
            pass

        page = requests.get(url, headers=get_headers())
        soup = BeautifulSoup(page.content, 'html.parser')
        
        try:
            title = soup.find(id="productTitle").get_text()
            price = soup.find(id="soldByThirdParty").get_text()
        except AttributeError:
            try:
                title = soup.find(id="productTitle").get_text()
                price = soup.find(id="priceblock_ourprice").get_text()
            except:
                return JsonResponse(data={"status": 500, "message": "Internal Service Error", "status":"Fixed Soon"})
        i=price.index('.')
        cov_p=price[2:i+3]
        price=float((re.sub(",","",cov_p)))
        title=title.replace('\n','')
        return JsonResponse(data={"status": 200, "title": str(title), "Price": str(price)})

    else:
        return JsonResponse(data={"status": 400, "message": "Get Request Not Allowed"})
