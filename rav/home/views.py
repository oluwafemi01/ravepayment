from django.shortcuts import render
from django.http import HttpResponse
import requests
import hashlib

# Create your views here.
seckey = "FLWSECK-99e69aab24c897470a3ace12dc40ff3b-X"
pb_key = "FLWPUBK-e618d594c3f4392a5d4242d7af86f201-X"
amount_in_naira = '1000'
customer_email = "user@example.com"
customer_firstname = "Temi"
customer_lastname = "Adelewa"
txref = '82993'
country = "NG"
currency = "NGN"

options = dict(PBFPubKey=pb_key, amount=amount_in_naira, country=country, currency=currency,
               customer_email=customer_email, customer_firstname=customer_firstname,
               customer_lastname=customer_lastname, txref=txref)


def ksort(d):
    return {i: d[i] for i in sorted(d.keys())}


def index(request):
    ksort(options)
    hashedpayload = ''.join(str(options[e]) for e in options)
    completehash = hashedpayload + seckey
    integrity = hashlib.sha256(completehash.encode('ascii')).hexdigest()
    user_home = "WELCOME PAGE"
    return render(request, 'home/index.html', {"title": user_home, "error": "", "integrity": integrity})


def verify(request):
    if request.method == "GET":
        flw_ref = request.GET['flw']
        data = {
            "flw_ref": flw_ref,
            "SECKEY": seckey,
            "normalize": "1"
        }

        url = "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/flwv3-pug/getpaidx/api/verify"

        # headers = {'content-type': 'application/json'}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(url, headers=headers, data=data)

        # print(r.json())
        # return HttpResponse(r.json(),content_type='application/json')
        return HttpResponse(r)
