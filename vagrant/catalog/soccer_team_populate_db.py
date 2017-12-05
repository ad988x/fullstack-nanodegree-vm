from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Teams, Base, User

engine = create_engine('sqlite:///itemcatalogwithuser.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


User1 = User(name="Andy Dusanowsky", email="duzy2172@gmail.com")
session.add(User1)
session.commit()


# Premier League Category
category1 = Category(name='Premier League', img_url='https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/Premier_League_Logo.svg/250px-Premier_League_Logo.svg.png', user_id=1)
session.add(category1)
session.commit()

teams1 = Teams(user_id=1, name='Tottenham Hotspur', location='Wembly Stadium',
               yr_strtd='1882', image_url='https://upload.wikimedia.org/'
               'wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/125px'
               '-Tottenham_Hotspur.svg.png')
session.add(teams1)
session.commit()

teams2 = Teams(user_id=1, name='Chelsea F.C.', location='Stamford Bridge',
               yr_strtd='1905', image_url='https://upload.wikimedia.org/'
               'wikipedia/en/thumb/c/cc/Chelsea_FC.svg/200px-Chelsea_FC.'
               'svg.png')
session.add(teams2)
session.commit()

teams3 = Teams(user_id=1, name='Liverpool F.C.', location='Anfield',
               yr_strtd='1892', image_url='https://upload.wikimedia.org/'
               'wikipedia/en/thumb/0/0c/Liverpool_FC.svg/170px-Liverpool_FC'
               '.svg.png')
session.add(teams3)
session.commit()

teams4 = Teams(user_id=1, name='Arsenal F.C.', location='Emirates Stadium',
               yr_strtd='1886', image_url='https://upload.wikimedia.org/'
               'wikipedia/en/thumb/5/53/Arsenal_FC.svg/180px-Arsenal_FC.'
               'svg.png')
session.add(teams4)
session.commit()


# La Liga Category
category2 = Category(name='La Liga', img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/LaLiga_Santander.svg/201px-LaLiga_Santander.svg.png', user_id=1)
session.add(category2)
session.commit()

teams5 = Teams(user_id=1, name='FC Barcelona', location='Camp Nou',
               yr_strtd='1899', image_url='https://upload.wikimedia.org/'
               'wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/220px-'
               'FC_Barcelona_%28crest%29.svg.png')
session.add(teams5)
session.commit()

teams6 = Teams(user_id=1, name='Real Madrid C.F.',
               location='Santiago Bernabeu Stadium', yr_strtd='1902',
               image_url='https://upload.wikimedia.org/wikipedia/en/thumb/5/'
               '56/Real_Madrid_CF.svg/165px-Real_Madrid_CF.svg.png')
session.add(teams6)
session.commit()

teams7 = Teams(user_id=1, name='Atletico Madrid',
               location='Wanda Metropolitano', yr_strtd='1903',
               image_url='https://upload.wikimedia.org/wikipedia/en/thumb/f/'
               'f4/Atletico_Madrid_2017_logo.svg/170px-Atletico_Madrid_2017'
               '_logo.svg.png')
session.add(teams7)
session.commit()

teams8 = Teams(user_id=1, name='Valencia CF', location='Mestalla Stadium',
               yr_strtd='1919', image_url='https://upload.wikimedia.org/'
               'wikipedia/en/thumb/c/ce/Valenciacf.svg/220px-Valenciacf.'
               'svg.png')
session.add(teams8)
session.commit()


# Major League Soccer Category
category3 = Category(name='Major League Soccer', img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/MLS_logo.svg/150px-MLS_logo.svg.png', user_id=1)
session.add(category3)
session.commit()

teams9 = Teams(user_id=1, name='LA Galaxy', location='StubHub Center',
               yr_strtd='1994', image_url='https://upload.wikimedia.org/'
               'wikipedia/en/thumb/7/70/Los_Angeles_Galaxy_logo.svg/220px-'
               'LosAngeles_Galaxy_logo.svg.png')
session.add(teams9)
session.commit()

teams10 = Teams(user_id=1, name='Seattle Sounders FC',
                location='CenturyLink Field', yr_strtd='2007',
                image_url='https://upload.wikimedia.org/wikipedia/en/thumb/2/'
                '27/Seattle_Sounders_FC.svg/170px-Seattle_Sounders_FC.svg.png')
session.add(teams10)
session.commit()

teams11 = Teams(user_id=1, name='D.C. United', location='Audi Field',
                yr_strtd='1996', image_url='https://upload.wikimedia.org/'
                'wikipedia/en/thumb/3/32/D.C._United_logo_%282016%29'
                '.svg/220px-D.C._United_logo_%282016%29.svg.png')
session.add(teams11)
session.commit()

teams12 = Teams(user_id=1, name='New York Red Bulls',
                location='Red Bull Arena', yr_strtd='1994',
                image_url='https://upload.wikimedia.org/'
                'wikipedia/en/thumb/5/51/New_York_Red_Bulls_logo.svg/230px-'
                'New_York_Red_Bulls_logo.svg.png')
session.add(teams12)
session.commit()


# German Bendesliga League Category
category4 = Category(name='Bundesliga; German League', img_url='https://upload.wikimedia.org/wikipedia/en/thumb/d/df/Bundesliga_logo_%282017%29.svg/190px-Bundesliga_logo_%282017%29.svg.png', user_id=1)
session.add(category4)
session.commit()

teams13 = Teams(user_id=1, name='FC Bayern Munich', location='Allianz Arena',
                yr_strtd='1900', image_url='https://upload.wikimedia.org/'
                'wikipedia/en/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017'
                '%29.svg/220px-FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg.png')
session.add(teams13)
session.commit()

teams14 = Teams(user_id=1, name='Borussia Dortmund', location='Westfale'
                'nstadion', yr_strtd='1909', image_url='https://upload.'
                'wikimedia.org/wikipedia/commons/thumb/6/67/Borussia_Dortmund_'
                'logo.svg/220px-Borussia_Dortmund_logo.svg.png')
session.add(teams14)
session.commit()

teams15 = Teams(user_id=1, name='SV Werder Bremen', location='Weserstadion',
                yr_strtd='1899', image_url='https://upload.wikimedia.org/'
                'wikipedia/commons/thumb/b/be/SV-Werder-Bremen-Logo.svg/'
                '125px-SV-Werder-Bremen-Logo.svg.png')
session.add(teams15)
session.commit()

teams16 = Teams(user_id=1, name='Hamburger SV', location='Volksparkstadion',
                yr_strtd='1887', image_url='https://upload.wikimedia.org/'
                'wikipedia/commons/thumb/6/66/HSV-Logo.svg/220px-HSV-Logo.'
                'svg.png')
session.add(teams16)
session.commit()


print "add all teams in catalog"
