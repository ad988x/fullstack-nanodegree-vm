from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Player, Team, Base, User

engine = create_engine('sqlite:///itemcatalogwithuser.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name="Andy Dusanowsky", email="duzy2172@gmail.com")
session.add(User1)
session.commit()


# Tottenham Hotspur Team
team1 = Team(name='Tottenham Hotspur', user_id=1)
session.add(team1)
session.commit()

player1 = Player(user_id=1, name='Harry Kane', origin='England',
                 yr_strtd='2004', position='Forward', team=team1)
session.add(player1)
session.commit()

player2 = Player(user_id=1, name='Dele Alli', origin='England',
                 yr_strtd='2015', position='Mid Field', team=team1)
session.add(player2)
session.commit()

player3 = Player(user_id=1, name='Hugo Lloris', origin='France',
                 yr_strtd='2012', position='Goal Keeper', team=team1)
session.add(player3)
session.commit()

player4 = Player(user_id=1, name='Danny Rose', origin='England',
                 yr_strtd='2007', position='Defense', team=team1)
session.add(player4)
session.commit()

player5 = Player(user_id=1, name='Son Heung-min', origin='South Korea',
                 yr_strtd='2015', position='Forward', team=team1)
session.add(player5)
session.commit()

player6 = Player(user_id=1, name='Christian Eriksen', origin='Denmark',
                 yr_strtd='2013', position='Mid Field', team=team1)
session.add(player6)
session.commit()

# Arsenal F.C. Team
team2 = Team(name='Arsenal F.C.', user_id=1)
session.add(team2)
session.commit()

player7 = Player(user_id=1, name='Alexis Sanchez', origin='Chile',
                 yr_strtd='2014', position='Forward', team=team2)
session.add(player7)
session.commit()

player8 = Player(user_id=1, name='Aaron Ramsey', origin='Wales',
                 yr_strtd='2008', position='Mid Field', team=team2)
session.add(player8)
session.commit()

player9 = Player(user_id=1, name='David Ospina Ramirez', origin='Columbia',
                 yr_strtd='2014', position='Goal Keeper', team=team2)
session.add(player9)
session.commit()

player10 = Player(user_id=1, name='Per Mertesacker', origin='West Germany',
                  yr_strtd='2011', position='Defense', team=team2)
session.add(player10)
session.commit()

player11 = Player(user_id=1, name='Alex Iwobi', origin='Nigeria',
                  yr_strtd='2015', position='Forward', team=team2)
session.add(player11)
session.commit()

player12 = Player(user_id=1, name='Jack Wilshere', origin='England',
                  yr_strtd='2008', position='Mid Field', team=team2)
session.add(player12)
session.commit()


# Chelsea F.C. Team
team3 = Team(name='Chelsea F.C.', user_id=1)
session.add(team3)
session.commit()

player13 = Player(user_id=1, name='Alvaro Morata', origin='Spain',
                  yr_strtd='2017', position='Forward', team=team3)
session.add(player13)
session.commit()

player14 = Player(user_id=1, name='Pedro', origin='Spain',
                  yr_strtd='2015', position='Mid Field', team=team3)
session.add(player14)
session.commit()

player15 = Player(user_id=1, name='Willy Caballero', origin='Argentina',
                  yr_strtd='2017', position='Goal Keeper', team=team3)
session.add(player15)
session.commit()

player16 = Player(user_id=1, name='Gary Cahil', origin='England',
                  yr_strtd='2012', position='Defense', team=team3)
session.add(player16)
session.commit()

player17 = Player(user_id=1, name='Michy Batshauayi', origin='Belgium',
                  yr_strtd='2016', position='Forward', team=team3)
session.add(player17)
session.commit()

player18 = Player(user_id=1, name='William', origin='Brazil',
                  yr_strtd='2013', position='Mid Field', team=team3)
session.add(player18)
session.commit()


# Liverpool F.C. Team
team4 = Team(name='Liverpool F.C.', user_id=1)
session.add(team4)
session.commit()

player19 = Player(user_id=1, name='Roberto Frimino', origin='Brazil',
                  yr_strtd='2015', position='Forward', team=team4)
session.add(player19)
session.commit()

player20 = Player(user_id=1, name='Georginio Wijnaldum', origin='Netherlands',
                  yr_strtd='2016', position='Mid Field', team=team4)
session.add(player20)
session.commit()

player21 = Player(user_id=1, name='Loris Karius', origin='Germany',
                  yr_strtd='2016', position='Goal Keeper', team=team4)
session.add(player21)
session.commit()

player22 = Player(user_id=1, name='Dejan Lovren', origin='SFR Yugoslavia',
                  yr_strtd='2014', position='Defense', team=team4)
session.add(player22)
session.commit()

player23 = Player(user_id=1, name='Daniel Sturridge', origin='England',
                  yr_strtd='2013', position='Forward', team=team4)
session.add(player23)
session.commit()

player24 = Player(user_id=1, name='Jordan Henderson', origin='England',
                  yr_strtd='2011', position='Mid Field', team=team4)
session.add(player24)
session.commit()


print "added all teams"
