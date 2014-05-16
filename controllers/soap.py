# -*- coding: utf-8 -*-

#from gluon.contrib.pysimplesoap.client import SoapClient
from suds.client import Client

def index():

    # Suds BEGIN
    url = "http://selma-test.its.uu.se/selmaws-uu/services/PlanTjanst?wsdl"
    client = Client(url);
    client.set_options(port="PlanTjanstHttpSoap11Endpoint")

    response = client.service.hamtaKursplanKurskod(kurskod="1MA025")
    namn = response['kurs']['namn']
    poang = response['kurs']['poang']
    fordjukod1 = response['kurs']['huvudomradeFordjupningar'][0]['fordjupningskod']#['fordjupningskod']#['huvudomrade']#['benamning']
    amne1 = response['kurs']['huvudomradeFordjupningar'][0]['huvudomrade']['benamning']
    fordjukod2 = ""
    amne2 = ""

#check om kursen innehåller två huvudämnen. if so så hämtar vi det andra huvudämnet
    gotdata = 1
    try:
        gotdata = response['kurs']['huvudomradeFordjupningar'][1]
    except IndexError:
        gotdata = 0
    if gotdata:
        fordjukod2 = response['kurs']['huvudomradeFordjupningar'][1]['fordjupningskod']#['fordjupningskod']#['huvudomrade']#['benamning']
        amne2 = response['kurs']['huvudomradeFordjupningar'][1]['huvudomrade']['benamning']
    
# lägg in allt i databasen!!!!
    

    print namn
    print poang
    print fordjukod1
    print amne1
    print fordjukod2
    print amne2

    #return dict(message=(namn, poang, fordjukod1, amne1, fordjukod2, amne2))
    #return dict(message=amne1)

