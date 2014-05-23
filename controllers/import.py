# -*- coding: utf-8 -*-
import json, os
from suds.client import Client

def index():
    #deleteKurs("1MA013")
    #insert("testjson.json", "Mol", "X", 2014)

    insert("x1415.json", "MolykularBioteknikC", "X", 2014)
    """
    insert("it1415.json", "InformationsteknologiC", "IT", 2014)
    insert("e1415.json", "ElektroteknikC", "E", 2014)
    insert("ei1415.json", "ElektroteknikH", "EI", 2014)
    insert("es1415.json", "EnergisystemC", "ES", 2014)
    insert("f1415.json", "TekniskfysikC", "F", 2014)
    insert("k1415.json", "KemiteknikC", "K", 2014)
    insert("mi1415.json", "MaskinteknikH", "MI", 2014)
    insert("b1415.json", "ByggteknikC", "B", 2014)
    insert("q1415.json", "TekniskfysikmedMaterialvetenskapC", "Q", 2014)
    insert("w1415.json", "MiljoVattenteknikC", "W", 2014)
    insert("sts1415.json", "SystemiteknikochSamhalleC", "STS", 2014)
    """
    #message = getinfoSelma("1MA009")
    #message = dict(message = )    
    #return dict(message = message)


def insert(filnamn, prognamn, progkort, ar):
    path = 'applications/coursefy/scripts/uuse/scraped/'
    # funktion som checkar om programmet och studieplanen finns sedan tidigare
    # här antas att om programmet inte finns så finns inte studieplanen
    id_studieplan = studieProgId(prognamn, progkort, ar)

    filnamn = path + filnamn
    with open(filnamn) as json_file:
        json_data = json.load(json_file)

        for row in json_data:
            #poang = row["credits"]
            kurskod = row["code"] 
            period = row["period"]
            #namn = row["name"]
            # om "period" är längre än 2 antar jag att elementet innehåller chars eller för många siffror
            if len(period) > 2:
                period = 0
            existList = existerarKurs(kurskod, progkort, period)
                # if-sats om det inte redan finns ett table för samma kurskod (kurs). Då går vi in och hämta all info om kursen i Selma
            if (existList[0] != True or existList[1] != True):
                attributList = getinfoSelma(kurskod)
                namn = row["name"]
                poang = row["credits"]
                niva = row["level"]
                if attributList == []:
                    attributList.append(namn)
                    attributList.append(poang)
                    attributList.append(niva)
                    attributList.append("")
                    attributList.append("")
                    attributList.append("")
                elif attributList[0] == "":
                    attributList[0] = name
                elif attributList[1] == 0:
                    for c in poang:
                        if c == "(":
                            temp = []
                            for c in poang:
                                if c == ")":
                                    for c in poang:
                                        if c == int:
                                            temp.append(c)
                            poang = temp
                    attributList[1] = poang
                elif attributList[2] == "":
                    attributList[2] = niva 
                id_niva = db.niva.insert(namn = attributList[2])
                id_kursplan = db.kursplan.insert(namn = attributList[0], kurskod = kurskod, poang = attributList[1], niva = id_niva)
                id_kurstillfalle = db.kurstillfalle.insert(kursplan = id_kursplan)
                db.perioder.insert(kurstillfalle = id_kurstillfalle, period = period)
                db.kurstillfalle_studieplan.insert(studieplan = id_studieplan, kurstillfalle = id_kurstillfalle, startperiod = period, slutperiod = period)
                laggTillAmne(id_kursplan, attributList[3], attributList[2])
                if(attributList[5] != ""):
                    laggTillAmne(id_kursplan, attributList[5], attributList[4])

def laggTillAmne(id_kursplan, amne, fordjukod):
    id_omradesklassning = ""
    id_djup = ""
    for row in db(db.omradesklassning.namn).select():
        id_omradesklassning = row.id
        break
    if(id_omradesklassning == ""): 
        id_omradesklassning = db.omradesklassning.insert(namn = amne)
    for row in db(db.djup.namn == fordjukod).select():
        id_djup = row.id
        break
    if(id_djup == ""):
        id_djup = db.djup.insert(namn = fordjukod) 
    db.omradesklassningar.insert(kursplan = id_kursplan, omradesklassning = id_omradesklassning, djup = id_djup)

def existerarKurs(kurskod, progkort, period):
    existerar_kurs = False
    existerar_studie = False
    # check för att se om vi redan har skapat ett table för den här kurskoden, isf sätts "existerar" till true vilket indikerar att
    # det redan finns ett table. Att det finns flera objekt med samma kurskod beror på att kursen går över flera perioder.
    for row in db(db.kursplan.kurskod == kurskod).select():
        existerar_kurs = True
        tillf_id_kursplan = row.id
        #print tillf_id_kursplan
        for row in db(db.kurstillfalle.kursplan == tillf_id_kursplan).select():
            tillf_id_kurstillfalle = row.id
            #print tillf_id_kurstillfalle
            for row in db(db.kurstillfalle_studieplan.kurstillfalle == tillf_id_kurstillfalle).select():
                tillf_studieplan = row.studieplan
                #print tillf_studieplan
                for row in db(db.studieplan.id == tillf_studieplan).select():
                    tillf_namn = row.namn
                    if tillf_namn == progkort:
                        existerar_studie = True
                        # Sätter om slutperioden för den existerande kurskoden (kursen)
                        for row in db(db.kurstillfalle_studieplan.kurstillfalle == tillf_id_kurstillfalle).select():
                            row.update_record(slutperiod = period)
                            break
                    break
                break
            break
        break
    existList = [existerar_kurs, existerar_studie]
    return existList

def updateKurs():
    #path = 'applications/coursefy/scripts/uuse/scraped/'
    filnamn = path + filnamn
    #import time
    #date = (time.strftime("%d/%m/%Y"))
    #print date
    with open(filnamn) as json_file:
        json_data = json.load(json_file)

def deleteKurs(kurskod):
    for row in db(db.kursplan.kurskod == kurskod).select():
        kursplan_id = row.id
        niva = row.niva
        break
    for row in db(db.kurstillfalle.kursplan == kursplan_id).select():
        kurstillfalle_id = row.id
        break
    for row in db(db.perioder.kurstillfalle == kurstillfalle_id).select():
        period_id = row.id
        break
    for row in db(db.niva.id == niva).select():
        niva_id = row.id
        break
    for row in db(db.kurstillfalle_studieplan.kurstillfalle == kurstillfalle_id).select():
        kurstillfalle_studieplan_id = row.id
        break 
    db(db.kurstillfalle_studieplan.id == kurstillfalle_id).delete()
    db(db.kurstillfalle.id == kurstillfalle_id).delete()
    db(db.perioder.id == period_id).delete()
    db(db.kursplan.id == kursplan_id).delete()
    db(db.niva.id == niva_id).delete()
    """
    print kursplan_id
    print kurstillfalle_id
    print period_id
    print niva_id
    print kurstillfalle_studieplan_id
    """

def studieProgId(prognamn, progkort, ar):
    id_studieplan = ""
    id_program = ""
    prog_exists = True
    studie_exists = True
    for row in db(db.program.namn).select():
        if db(db.program.namn == progkort).select():
            id_program = row.id
            prog_exists = False
            for row in db(db.studieplan.ar).select():
                if db(db.studieplan.ar == ar).select():
                    id_studieplan = row.id
                    studie_exists = False
                break
        break
    if prog_exists:    
        id_program = db.program.insert(namn = progkort, beskrivning = prognamn)
    if studie_exists:
        id_studieplan = db.studieplan.insert(namn = progkort, beskrivning = prognamn, program = id_program, ar = ar)
    return id_studieplan


def getinfoSelma(kurskod):
    # Suds BEGIN
    url = "http://selma-test.its.uu.se/selmaws-uu/services/PlanTjanst?wsdl"
    client = Client(url);
    client.set_options(port="PlanTjanstHttpSoap11Endpoint")
   # print "kurskod: " + kurskod
    response = client.service.hamtaKursplanKurskod(kurskod=kurskod)
    
    # check för om kursen inte finns i Selma
    namn = 1
    poang = 1
    fordjukod1 = 1
    amne1 = 1

    try:
        test = response['kurs']
    except TypeError:
        return []
        #kursen finns i Selma!!!
    try:
        test_namn = response['kurs']['namn']
    except TypeError:
        namn = ""
    if namn:
        namn = response['kurs']['namn']
    try:
        test_poang = response['kurs']['poang']
    except TypeError:
        poang = 0
    if poang:
        poang = response['kurs']['poang']
        # varibler för att plocka ut huvudämne
    try:
        test_fordjukod1 = response['kurs']['huvudomradeFordjupningar'][0]['fordjupningskod']
    except TypeError:
        fordjukod1 = ""
    if fordjukod1:
        fordjukod1 = response['kurs']['huvudomradeFordjupningar'][0]['fordjupningskod']
    try:
        test_amne1 = response['kurs']['huvudomradeFordjupningar'][0]['huvudomrade']['benamning']
    except TypeError:
        amne1 = ""
    if amne1:
        amne1 = response['kurs']['huvudomradeFordjupningar'][0]['huvudomrade']['benamning']
        # variabler för att plocka ut dubbla huvudämnen
    fordjukod2 = ""
    amne2 = ""
        # check om kursen innehåller två huvudämnen. if so hämtar vi det andra huvudämnet
    gotdata = 1
    try:
        gotdata = response['kurs']['huvudomradeFordjupningar'][1]
    except IndexError:
        gotdata = 0
    if gotdata:
        fordjukod2 = response['kurs']['huvudomradeFordjupningar'][1]['fordjupningskod']                                            
        amne2 = response['kurs']['huvudomradeFordjupningar'][1]['huvudomrade']['benamning']
    # början på funktion för att kolla när selma senast var uppdaterad
    #try:
    #    senast_uppd = response['kurs'][]
    returnlist = [namn, poang, fordjukod1, amne1, fordjukod2, amne2]

    #printsats för lokal testning
    """
    print namn
    print poang
    print fordjukod1
    print amne1
    print fordjukod2
    print amne2
    print returnlist[0]
    """
    return returnlist


"""
# program som har scrapats

insert("it1415.json", "InformationsteknologiC", "IT", 2014)

insert("e1415.json", "ElektroteknikC", "E", 2014)
insert("ei1415.json", "ElektroteknikH", "EI", 2014)
insert("es1415.json", "EnergisystemC", "ES", 2014)
insert("f1415.json", "TekniskfysikC", "F", 2014)
insert("k1415.json", "KemiteknikC", "K", 2014)
insert("mi1415.json", "MaskinteknikH", "MI", 2014)
insert("q1415.json", "TekniskfysikmedMaterialvetenskapC", "Q", 2014)
insert("sts1415.json", "SystemiteknikochSamhalleC", "STS", 2014)


#program vi inte har scrapat än
insert("it1213.json", "InformationsteknologiC", "IT", 2012)
insert("it1314.json", "InformationsteknologiC", "IT", 2013)
insert("it1415.json", "InformationsteknologiC", "IT", 2014)
insert("e1213.json", "ElektroteknikC", "E", 2012)
insert("e1314.json", "ElektroteknikC", "E", 2013)
insert("es1213.json", "EnergisystemC", "ES", 2012)
insert("es1314.json", "EnergisystemC", "ES", 2013)
insert("k1213.json", "KemiteknikC", "K", 2012)
insert("k1314.json", "KemiteknikC", "K", 2013)
insert("w1213.json", "MiljoVattenteknikC", "W", 2012)
insert("w1314.json", "MiljoVattenteknikC", "W", 2013)
insert("x1213.json", "MolykularBioteknikC", "X", 2012)
insert("x1314.json", "MolykularBioteknikC", "X", 2013)
insert("sts1213.json", "SystemiteknikochSamhalleC", "STS", 2012)
insert("sts1314.json", "SystemiteknikochSamhalleC", "STS", 2013)
insert("f1213.json", "TekniskfysikC", "F", 2012)
insert("f1314.json", "TekniskfysikC", "F", 2013)
insert("q1213.json", "TekniskfysikmedMaterialvetenskapC", "Q", 2012)
insert("q1314.json", "TekniskfysikmedMaterialvetenskapC", "Q", 2013)
insert("b1213.json", "ByggteknikC", "B", 2012)
insert("b1314.json", "ByggteknikC", "B", 2013)
insert("ei1213.json", "ElektroteknikH", "EI", 2012)
insert("ei1314.json", "ElektroteknikH", "EI", 2013)
insert("mi1213.json", "MaskinteknikH", "MI", 2012)
insert("mi1314.json", "MaskinteknikH", "MI", 2013)
insert("1415.json", "KvalitetsutvecklingochLedarskap", "", 2014)
insert("kki1213.json", "KarnkraftteknikH", "KKI", 2012)
insert("kki1314.json", "KarnkraftteknikH", "KKI", 2013)
insert("kki1415.json", "KarnkraftteknikH", "KKI", 2014)
insert("nvb1213.json", "BiologiNM", "NVB", 2012)
insert("nvb1314.json", "BiologiNM", "NVB", 2013)
insert("nvb1415.json", "BiologiNM", "NVB", 2014)
insert("dv1213.json", "DatavetenskapNM", "DV", 2012)
insert("dv1314.json", "DatavetenskapNM", "DV", 2013)
insert("dv1415.json", "DatavetenskapNM", "DV", 2014
insert("nvf1213.json", "FysikNM", "NVF", 2012)
insert("nvf1314.json", "FysikNM", "NVF", 2013)
insert("nvf1415.json", "FysikNM", "NVF", 2014)
insert("nvg1213.json", "GeovetenskapNM", "NVG", 2012)
insert("nvg1314.json", "GeovetenskapNM", "NVG", 2013)
insert("nvg1415.json", "GeovetenskapNM", "NVG", 2014) 
insert("1213.json", "HallbarUtvecklingNM", "", 2012)
insert("1314.json", "HallbarUtvecklingNM", "", 2013)
insert("1415.json", "HallbarUtvecklingNM", "", 2014)
insert("nvk1213.json", "KemiNM", "NVK", 2012)
insert("nvk1314.json", "KemiNM", "NVK", 2013) 
insert("nvk1415.json", "KemiNM", "NVK", 2014)
insert("nvm1213.json", "MatematikNM", "NVM", 2012)
insert("nvm1314.json", "MatematikNM", "NVM", 2013)
insert("nvm1415.json", "MatematikNM", "NVM", 2014) 
insert("1213.json", "TillampadberakningsvetenskapNM", "", 2012)
insert("1314.json", "TillampadberakningsvetenskapNM", "", 2013) 
insert("1415.json", "TillampadberakningsvetenskapNM", "", 2014) 
insert("1213.json", "TillampadBioteknikNM", "", 2012)
insert("1314.json", "TillampadBioteknikNM", "", 2013)
insert("1415.json", "TillampadBioteknikNM", "", 2014) 
insert("1213.json", "BioinformationTM", "", 2012)
insert("1314.json", "BioinformationTM", "", 2013)
insert("1415.json", "BioinformationTM", "", 2014)
insert("1213.json", "FornybarElgenereringTM", "", 2012)
insert("1314.json", "FornybarElgenereringTM", "", 2013)
insert("1415.json", "FornybarElgenereringTM", "", 2014) 
insert("1213.json", "InbyggdaSystemTM", "", 2012)
insert("1314.json", "InbyggdaSystemTM", "", 2013)
insert("1415.json", "InbyggdaSystemTM", "", 2014) 
insert("1213.json", "IndustriellLedningochInovationTM", "", 2012)
insert("1314.json", "IndustriellLedningochInovationTM", "", 2013)
insert("1415.json", "IndustriellLedningochInovationTM", "", 2014) 
insert("1213.json", "MolekylarBioteknikTM", "", 2012)
insert("1314.json", "MolekylarBioteknikTM", "", 2013)
insert("1415.json", "MolekylarBioteknikTM", "", 2014) 
insert("1213.json", "EnergiteknikTM", "", 2012)
insert("1314.json", "EnergiteknikTM", "", 2013)
insert("1415.json", "EnergiteknikTM", "", 2014)
"""