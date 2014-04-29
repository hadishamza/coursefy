db = DAL('mysql://username:password@localhost/test')

db.define_table('Program'
                db.Field('id'),
                db.Field('namn'),
                db.Field('beskrivning'))