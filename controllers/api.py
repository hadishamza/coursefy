import json

@request.restful()
def courses():
    response.view = 'generic.json'
    def GET(searchword):
        kurser = db(db.kursplan.kurskod.contains(searchword) | db.kursplan.namn.contains(searchword)).select(limitby=(0,5))
        if not kurser:
            raise HTTP(404)
        return kurser.json()
    return locals()

@request.restful()
def user_studyplan():
    response.view = 'generic.json'
    def GET(id):
        studyplan = db(db.api_studieplan.key==id).select().first()
        print studyplan
        if not studyplan:
            raise HTTP(404)

        else:
            return studyplan

    def POST(id, parent_id, user_studyplan):
        if is_json(user_studyplan):
            parent = db(db.api_studieplan.key==parent_id).select().first()
            if parent:
                parent_id = parent['key']
            else:
                parent_id = None
            studyplan_id = db.api_studieplan.insert(parent=parent, value=user_studyplan)

            if studyplan_id:
                return {'uuid': db.api_studieplan(studyplan_id).key}
            else:
                raise HTTP(500)

    def PUT(id, user_studyplan):
        if is_json(user_studyplan):
            study = db(db.api_studieplan.key==id).select().first()
            if study:
                study = db(db.api_studieplan.key==id).update(value=user_studyplan)
                return study
            else:
                raise HTTP(404)
        else:
            raise HTTP(400)

    return locals()

@request.restful()
def studyplan():
    response.view = 'generic.json'
    def GET(studyplan_id):
        studyplan = db(db.studieplan.id==studyplan_id).select().first()
        if not studyplan:
            raise HTTP(404)

        rows = db(db.kurstillfalle_studieplan.studieplan==studyplan.id).select()
        if not rows:
            raise HTTP(500)

        data = []
        for row in rows:
            kursplan = row.kurstillfalle.kursplan
            course = {}
            course['credits'] = kursplan.poang
            course['level'] = kursplan.niva.namn
            course['code'] = kursplan.kurskod
            course['period'] = row.startperiod
            course['extended'] = False
            course['name'] = kursplan.namn
            course['examination'] = kursplan.examination
            course['requirements'] = kursplan.behorighet

            if row.startperiod != row.slutperiod:
                course['extended'] = True

            data.append(course)

        return json.dumps(data)
    return locals()

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True