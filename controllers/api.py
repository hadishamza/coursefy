@request.restful()
def courses():
    response.view = 'generic.json'
    def GET(searchword):
    	kurser = kursplan = db(db.kursplan.kurskod.contains(searchword)).select(limitby=(0,5))
        return kurser.json()
    return locals()

