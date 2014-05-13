# -*- coding: utf-8 -*-
import json

def index():
    insert("it1415.json", "InformationsteknologiC", "IT", 2014)
    message = "hej"
    return dict(message=message)

def insert(filnamn, prognamn, progkort, ar):
    id_program = db.program.insert(namn = progkort, beskrivning = prognamn)
    id_studieplan = db.studieplan.insert(namn = progkort, beskrivning = prognamn, program = id_program, ar = ar)

    with open(filnamn) as json_file:
        json_data = json.load(json_file)

        for row in json_data:
            kurskod = row["code"]
            period = row["period"]
            existerar = False
            for row in db(db.kursplan.kurskod == kurskod).select():
                id_kursplan = row.id
                existerar = True
                for row in db(db.kurstillfalle.kursplan == id_kursplan).select():
                    kurstillfalle = row.id
                    for rowrow in db(db.kurstillfalle_studieplan.kurstillfalle == kurstillfalle).select():
                        rowrow.update_record(slutperiod = period)
                break
            if existerar != True:
                id_kursplan = db.kursplan.insert(kurskod = kurskod)
                id_kurstillfalle = db.kurstillfalle.insert(kursplan = id_kursplan)
                db.perioder.insert(kurstillfalle = id_kurstillfalle, period = period)
                db.kurstillfalle_studieplan(kurstillfalle = id_kurstillfalle, startperiod = period, slutperiod = period, studieplan = id_studieplan)
