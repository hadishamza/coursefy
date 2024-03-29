import uuid

db = DAL('sqlite://storage.db')

db.define_table('institution',
                Field('namn', 'string', length=255),
                Field('beskrivning', 'string', length=1023))

db.define_table('larare',
                Field('namn', 'string', length=255),
                Field('beskrivning', 'string', length=1023))

db.define_table('inriktning',
                Field('namn', 'string', length=255),
                Field('beskrivning', 'string', length=1023))

db.define_table('samlasning',
                Field('namn', 'string', length=255),
                Field('beskrivning', 'string', length=1023))

db.define_table('niva',
                Field('namn', 'string', length=255),
                Field('beskrivning', 'string', length=1023))

db.define_table('djup',
                Field('namn', 'string', length=255),
                Field('beskrivning', 'string', length=1023))

db.define_table('program',
                Field('namn', 'string', length=255,),
                Field('beskrivning', 'string', length=1023))

db.define_table('studieplan',
                Field('namn', 'string', length=255),
                Field('beskrivning', 'string', length=1023),
                Field('program', 'reference program'),
                Field('ar', 'integer'))

db.define_table('kursegenskap',
                Field('namn', 'string', length=255),
                Field('beskrivning', 'string', length=1023),
                Field('varde', 'integer'),
                Field('vardenamn', 'string', length=255),
                Field('vardebeskrivning', 'string', length=1023))

db.define_table('kursrelation',
                Field('namn', 'string', length = 255),
                Field('beskrivning', 'string', length = 1023))

db.define_table('omradesklassning',
                Field('namn', 'string', length = 255),
                Field('beskrivning', 'string', length = 1023))

db.define_table('betygsskala',
                Field('namn', 'string', length = 255),
                Field('beskrivning', 'string', length = 1023))

db.define_table('kursplan',
                Field('namn', 'string', length = 255),
                Field('poang', 'float'),
                Field('kurskod', 'string', length = 255),
                Field('beslutsdatum', 'date'),
                Field('behorighet', 'string', length = 255),
                Field('niva', 'reference niva', 'integer'),
                Field('betygsskala', 'reference betygsskala', 'integer'),
                Field('galler_fran', 'date'),
                Field('institution', 'reference institution', 'integer'),
                Field('mal', 'string', length = 1023),
                Field('innehall', 'string', length = 1023),
                Field('undervisning', 'string', length = 1023),
                Field('examination', 'string', length = 1023),
                Field('kurslitteratur', 'string', length = 1023))

db.define_table('kurstillfalle', # kursplan_studieplan? döpa om för att underlätta relationskopplingen?
                Field('kursplan', 'reference kursplan', 'integer', notnull = True),
                Field('anmalningskod', 'string', length = 255),
                Field('fart', 'integer'),
                Field('larare', 'reference larare', 'integer'))

db.define_table('larare_kurstillfalle',
                db.Field('larare', 'reference larare', notnull=True),  #not null
                db.Field('kurstillfalle', 'reference kurstillfalle', 'integer', notnull=True)) #not null

db.define_table('perioder',
                Field('kurstillfalle', 'reference kurstillfalle', notnull = True),
                Field('period', 'integer', notnull = True))

db.define_table('institution_kursplan',
                db.Field('institution', 'reference institution', notnull=True), #not null
                db.Field('kursplan', 'reference kursplan', 'integer',notnull=True)) #not null

db.define_table('kurstillfalle_studieplan',
                Field('studieplan', 'reference studieplan', notnull = True),
                Field('kurstillfalle', 'reference kurstillfalle', notnull = True),
                Field('obligatorisk', 'integer'),
                Field('startperiod', 'integer'),
                Field('slutperiod', 'integer'),
                Field('inriktning', 'reference inriktning'),
                Field('beskrivning', 'string', length = 1023))

db.define_table('kursrelationer',
                Field('kursrelation', 'reference kursrelation', notnull = True),
                Field('kalla', 'reference kurstillfalle', notnull = True),
                Field('mal', 'reference kurstillfalle', notnull = True),
                Field('dubbelinriktning', 'integer'))

db.define_table('kursegenskaper',
                Field('kursegenskaper', 'reference kursegenskap', notnull = True),
                Field('kurstillfalle', 'reference kurstillfalle', notnull = True),
                Field('varde', 'integer'))

db.define_table('samlasningar',
                Field('samlasning', 'reference samlasning', notnull = True),
                Field('program', 'reference program', notnull = True),
                Field('kurstillfalle', 'reference kurstillfalle', notnull = True))

db.define_table('overlappning',
                Field('kursplan1', 'reference kursplan', notnull = True),
                Field('kursplan2', 'reference kursplan', notnull = True))

db.define_table('omradesklassningar',
                Field('kursplan', 'reference kursplan', notnull = True),
                Field('omradesklassning', 'reference omradesklassning', notnull = True),
                Field('djup', 'reference djup', notnull = True))

### API ###
db.define_table('api_studieplan',
                Field('key', 'text', notnull = True, length=64, default=uuid.uuid4, unique=True), # link string
                Field('parent', 'reference api_studieplan'),
                Field('name', 'text'),
                Field('value', 'json', notnull = True)) # json value
