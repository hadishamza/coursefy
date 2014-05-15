# -*- coding: utf-8 -*-

#from gluon.contrib.pysimplesoap.client import SoapClient
from suds.client import Client

def index():

    # Suds BEGIN
    url = "http://selma-test.its.uu.se/selmaws-uu/services/PlanTjanst?wsdl"
    client = Client(url);
    client.set_options(port="PlanTjanstHttpSoap11Endpoint")

    response = client.service.hamtaKursplanKurskod(kurskod="1MA025")
    fordjukod1 = response['kurs']['huvudomradeFordjupningar'][2]#['fordjupningskod']#['huvudomrade']#['benamning']
    namnfordju1 = response['kurs']['huvudomradeFordjupningar'][3][1]


    print result

    return dict(message=result)

