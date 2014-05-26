import json

@request.restful()
def courses():
    response.view = 'generic.json'
    def GET(searchword):
        rows = db(db.kursplan.kurskod.contains(searchword) | db.kursplan.namn.contains(searchword)).select(limitby=(0,5))
        kurser = []
        for kursplan in rows:
            course = course_help(kursplan)
            course['period'] = None
            kurser.append(course)

        if not kurser:
            raise HTTP(404)
        return json.dumps(kurser)
    return locals()

@request.restful()
def user_studyplan():
    response.view = 'generic.json'
    def GET(id):
        studyplan = db(db.api_studieplan.key==id).select().first()
        if not studyplan:
            raise HTTP(404)

        else:
            return {'value': json.loads(studyplan.value), 'name': studyplan.name}

    def POST(user_studyplan, parent_id, name):
        if is_json(user_studyplan):
            if parent_id:
                parent = db(db.api_studieplan.key==parent_id).select().first()
            if parent:
                parent_id = parent['key']
            else:
                parent_id = None
            studyplan_id = db.api_studieplan.insert(parent=parent, value=user_studyplan, name=name)

            if studyplan_id:
                return {'uuid': db.api_studieplan(studyplan_id).key}
            else:
                raise HTTP(500)

    def PUT(key, user_studyplan, name):
        if is_json(user_studyplan):
            study = db(db.api_studieplan.key==key).select().first()
            if study:
                study.update_record(value=user_studyplan, name=name)
                return {'uuid': study.key}

            else:
                raise HTTP(404)
        else:
            raise HTTP(400)

    return locals()

@request.restful()
def studyplan_search():
    def GET(name):
        studyplans = db(db.studieplan.namn.contains(name)| db.studieplan.beskrivning.contains(name)).select(limitby=(0,5))
        return studyplans.json()
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
            course = course_help(kursplan)
            course['period'] = row.startperiod
            course['obl'] = row.obligatorisk
            course['extended'] = False

            if row.startperiod != row.slutperiod:
                course['extended'] = True

            data.append(course)
        ret = {'name': studyplan.beskrivning, 'value': data}
        return json.dumps(ret)
    return locals()

def course_help(kursplan):
    course = {}
    course['credits'] = kursplan.poang or ""
    course['level'] = kursplan.niva.namn or ""
    course['code'] = kursplan.kurskod
    course['extended'] = False
    course['subjects'] = ""
    course['name'] = kursplan.namn
    course['examination'] = kursplan.examination or ""
    course['requirements'] = kursplan.behorighet or ""
    kursplan_id = kursplan.id
    first = True
    for row in db(db.omradesklassningar.kursplan == kursplan_id).select():
        if not first:
            course['subjects'] += ", "
        else:
            first = False
        course['subjects'] += row.omradesklassning.namn


    return course

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True