@request.restful()
def studyplan():
    response.view = 'generic.json'
    def GET(program, year):
        if not tablename=='larare':
        	raise HTTP(400)
        return dict(larare = db.larare(id))
    return locals()