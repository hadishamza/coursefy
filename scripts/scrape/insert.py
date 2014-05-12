def insert(filnamn, prognamn, progkort, ar):

	import json

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
				for row in db(db.kurstillfalle.kursplan == id_kursplan).select()
					kurstillfalle = row.id
					for row in db(db.kurstillfalle_studieplan.kurstillfalle == kurstillfalle).select()
						row.update_record(slutperiod = period)
				break
			if existerar != True
				id_kursplan = db.kursplan.insert(kurskod = kurskod)
				id_kurstillfalle = db.kurstillfalle.insert(kursplan = id_kursplan)
				db.perioder.insert(kurstillfalle = id_kurstillfalle, period = period)
				db.kurstillfalle_studieplan(kurstillfalle = id_kurstillfalle, startperiod = period, slutperiod = period, studieplan = id_studieplan)


""" 
insert("it1213.json", "InformationsteknologiC", "IT", 2012)
insert("it1314.json", "InformationsteknologiC", "IT", 2013)
"""
insert("it1415.json", "InformationsteknologiC", "IT", 2014)
"""
insert("e1213.json", "ElektroteknikC", "E", 2012)
insert("e1314.json", "ElektroteknikC", "E", 2013)
insert("e1415.json", "ElektroteknikC", "E", 2014)
insert("es1213.json", "EnergisystemC", "ES", 2012)
insert("es1314.json", "EnergisystemC", "ES", 2013)
insert("es1415.json", "EnergisystemC", "ES", 2014)
insert("k1213.json", "KemiteknikC", "K", 2012)
insert("k1314.json", "KemiteknikC", "K", 2013)
insert("k1415.json", "KemiteknikC", "K", 2014)
insert("w1213.json", "MiljoVattenteknikC", "W", 2012)
insert("w1314.json", "MiljoVattenteknikC", "W", 2013)
insert("w1415.json", "MiljoVattenteknikC", "W", 2014)
insert("x1213.json", "MolykularBioteknikC", "X", 2012)
insert("x1314.json", "MolykularBioteknikC", "X", 2013)
insert("x1415.json", "MolykularBioteknikC", "X", 2014)
insert("sts1213.json", "SystemiteknikochSamhalleC", "STS", 2012)
insert("sts1314.json", "SystemiteknikochSamhalleC", "STS", 2013)
insert("sts1415.json", "SystemiteknikochSamhalleC", "STS", 2014) 
insert("f1213.json", "TekniskfysikC", "F", 2012)
insert("f1314.json", "TekniskfysikC", "F", 2013)
insert("f1415.json", "TekniskfysikC", "F", 2014)
insert("q1213.json", "TekniskfysikmedMaterialvetenskapC", "Q", 2012)
insert("q1314.json", "TekniskfysikmedMaterialvetenskapC", "Q", 2013)
insert("q1415.json", "TekniskfysikmedMaterialvetenskapC", "Q", 2014)
insert("b1213.json", "ByggteknikC", "B", 2012)
insert("b1314.json", "ByggteknikC", "B", 2013)
insert("b1415.json", "ByggteknikC", "B", 2014)
insert("ei1213.json", "ElektroteknikH", "EI", 2012)
insert("ei1314.json", "ElektroteknikH", "EI", 2013)
insert("ei1415.json", "ElektroteknikH", "EI", 2014)
insert("mi1213.json", "MaskinteknikH", "MI", 2012)
insert("mi1314.json", "MaskinteknikH", "MI", 2013)
insert("mi1415.json", "MaskinteknikH", "MI", 2014)
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
insert("1213.json", "HållbarUtvecklingNM", "", 2012)
insert("1314.json", "HållbarUtvecklingNM", "", 2013)
insert("1415.json", "HållbarUtvecklingNM", "", 2014)
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