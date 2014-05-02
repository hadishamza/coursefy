db = DAL('sqlite://storage.db')

db.define_table('institution',
                db.Field('namn', 'string', length=255),
                db.Field('beskrivning', 'string', length=1023))

db.define_table('institution_kursplan',
                db.Field('institution', 'reference institution', notnull=True), #not null
                db.Field('kursplan', 'integer',notnull=True)) #not null

db.define_table('larare_kurstillfälle',
                db.Field('larare', 'reference larare', notnull=True),  #not null
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
                db.Field('program', 'reference program'))

db.define_table('kursegenskap',
                db.Field('namn', 'string', length=255),
                db.Field('beskrivning', 'string', length=1023),
                db.Field('varde', 'integer'),
                db.Field('vardenamn', 'string', length=255),
                db.Field('vardebeskrivning', 'string', length=1023))

db.define_table('kursrelation', 
                Field('namn', 'string', length = 255), 
                Field('beskrivning', 'string', length = 1023))

db.define_table('omradesklassning', 
                Field('namn', 'string', length = 255), 
                Field('beskrivning', 'string', lenght = 1023))

db.define_table('betygsskala', 
                Field('namn', 'string', lenght = 255), 
                Field('beskrivning', 'string' lenght = 1023))

db.define_table('perioder', 
                Field('kurstillfalle', 'reference kurstillfalle'), 
                Field('period', 'integer'))

db.define_table('kursplan', 
                Field('namn', 'string', lenght = 255), 
                Field('poang', 'integer'), 
                Field('kurskod', 'string', lenght = 255), 
                Field('beslutsdatum', 'date'), 
                Field('behorighet', 'string', lenght = 255), 
                Field('niva', 'integer'), 
                Field('betygsskala', 'integer'), 
                Field('galler_fran', 'date'), 
                Field('institution', 'integer'), 
                Field('mal', 'string', lenght = 1023), 
                Field('innehall', 'string', length = 1023), 
                Field('undervisning', 'string', lenght = 1023), 
                Field('examination', 'string', lenght = 1023), 
                Field('kurslitteratur', 'string', lenght = 1023))

db.define_table('kurstillfalle', 
                Field('kursplan', 'integer'), 
                Field('anmalningskod', 'string', lenght = 255), 
                Field('fart', 'integer'), Field('larare', 'integer'))

db.define_table('kurstillfalle_studieplan', 
                Field('studieplan', 'reference studieplan'), 
                Field('kurstillfalle', 'reference kurstillfalle'), 
                Field('obligatorisk', 'integer'), 
                Field('startperiod', 'integer'), 
                Field('inriktning', 'refenrece inriktning'), 
                Field('beskrivning', 'string', lenght = 1023))

db.define_table('kursrelationer', 
                Field('kursrelation', 'reference kursrelation'), 
                Field('kalla', 'reference kurstillfalle'), 
                Field('mal', 'reference kurstillfalle'), 
                Field('dubbelinriktning', 'integer'))

db.define_table('kursegenskaper', 
                Field('kursegenskaper', 'reference kursegenskap'), 
                Field('kurstillfalle', 'reference kurstillfalle'),
                Field('varde', 'integer'))

db.define_table('samlasningar', 
                Field('samlasning', 'reference samlasning'), 
                Field('program', 'reference program'), 
                Field('kurstillfalle', 'reference kurstillfalle'))

db.define_table('overlappning', 
                Field('kursplan1', 'reference kursplan'), 
                Field('kursplan2', 'reference kursplan'))

db.define_table('omradesklassningar', 
                Field('kursplan', 'reference kursplan'), 
                Field('omradesklassning', 'omradesklassning'), 
                Field('djup', 'reference djup'))