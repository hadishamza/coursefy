db = DAL('sqlite://storage.db')

db.define_table('institution',
                db.Field('namn', 'string', length=255),
                db.Field('beskrivning', 'string', length=1023))

db.define_table('institution_kursplan',
                db.Field('institution', 'integer',notnull=True), #not null
                db.Field('kursplan', 'integer',notnull=True)) #not null

db.define_table('larare_kurstillfälle',
                db.Field('larare', 'integer', notnull=True),  #not null
                db.Field('kurstillfalle', 'integer', notnull=True)) #not null

db.define_table('inriktning',
                db.Field('namn', 'string', length=255),
                db.Field('beskrivning', 'string', length=1023))

db.define_table('samlasning',
                db.Field('namn', 'string', length=255),
                db.Field('beskrivning', 'string', length=1023))

db.define_table('larare',
                db.Field('namn', 'string', length=255),
                db.Field('beskrivning', 'string', length=1023))

db.define_table('niva',
                db.Field('namn', 'string', length=255),
                db.Field('beskrivning', 'string', length=1023))

db.define_table('djup',
                db.Field('namn', 'string', length=255),
                db.Field('beskrivning', 'string', length=1023))

db.define_table('program',
                db.Field('namn', 'string', length=255,),
                db.Field('beskrivning', 'string', length=1023))

db.define_table('studieplan',
                db.Field('namn', 'string', length=255),
                db.Field('beskrivning', 'string', length=1023),
                db.Field('program', 'integer'))

db.define_table('kursegenskap',
                db.Field('namn', 'string', length=255),
                db.Field('beskrivning', 'string', length=1023),
                db.Field('varde', 'integer'),
                db.Field('vardenamn', 'string', length=255),
                db.Field('vardebeskrivning', 'string', length=1023))
