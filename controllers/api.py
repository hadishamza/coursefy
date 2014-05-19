@request.restful()
def courses():
    response.view = 'generic.json'
    def GET(searchword):
        kurser = kursplan = db(db.kursplan.kurskod.contains(searchword)).select(limitby=(0,5))
        return kurser.json()
    return locals()

@request.restful()
def user_studyplan():
    response.view = 'generic.json'
    def GET(id):
        return None

    def POST(id, user_studyplan):
        return None
    return locals()

@request.restful()
def studyplan():
    response.view = 'generic.json'
    def GET(id):
        return None
    return locals()
