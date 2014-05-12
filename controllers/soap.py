# -*- coding: utf-8 -*-

#from gluon.contrib.pysimplesoap.client import SoapClient
from suds.client import Client

def index():

    # Suds BEGIN
    url = "http://selma-test.its.uu.se/selmaws-uu/services/PlanTjanst?wsdl"
    client = Client(url);
    client.set_options(port="PlanTjanstHttpSoap11Endpoint")

    response = client.service.hamtaKursplanKurskod(kurskod="1MA025")
    result = response['kurs']['namn']

    return dict(message=result)

