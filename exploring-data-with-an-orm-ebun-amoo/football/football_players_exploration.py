from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy import select, create_engine, func
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Player(Base):
    __tablename__ = "Players"
    id = Column(Integer, primary_key=True)
    name = Column(String())
    name_normalized = Column(String())
    caps = Column(Integer)
    goals = Column(Integer)
    most_recent_year_played = Column(Integer)
    position = Column(String())
    year_born = Column(Integer)
    club = Column(String())
    club_nationality = Column(String())
    played_in_latest = Column(String())
    country_id = Column(Integer, ForeignKey("countries.country_id"))
    
class Country(Base):
    __tablename__ = "Countries"
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String())


class FootballPlayersExploration:
    def __init__(self, filename):
        self.engine = create_engine(f'sqlite:///{filename}', echo=False)
        Session = sessionmaker(self.engine)
        self.session = Session()
    
    def save(self):
        self.session.commit()
            
    def get_most_goals(self):
        result = (
            self.session.query(Player)
            .order_by(Player.goals.desc())
            .first())
            
        print(f'Found: {result.name} - {result.goals}')
        
    def get_country_most_goals(self):
        player_id = (
            self.session.query(Player)
            .order_by(Player.goals.desc())
            .first()
        ).id
        id_country = (self.session.get(Player, player_id )).country_id
        result = self.session.get(Country, id_country)
        print(f"\n{result.country_name}")

    def most_caps(self):
        results = (
            self.session.query(Player)
            .order_by(Player.caps.desc())
            .limit(10)
            .all()
            )
        for result in results:
            print(f"\n{result.name} - {result.caps} caps")

    def country_most_goals(self):
        subquery = (
            self.session.query(Player.country_id, func.sum(Player.goals).label('total_goals'))
            .group_by(Player.country_id)
            .subquery())
        
        result = (
            self.session.query(Country.country_name, subquery.c.total_goals)
            .join(subquery, Country.country_id == subquery.c.country_id)
            .order_by(subquery.c.total_goals.desc())
            .first())
        
        print(f"\n{result[0]} - {result[1]} goals")
        

if __name__ == '__main__':
    footballPlayersExploration = FootballPlayersExploration('football_players_exploration.db')
    footballPlayersExploration.get_most_goals()
    footballPlayersExploration.get_country_most_goals()
    footballPlayersExploration.most_caps()
    footballPlayersExploration.country_most_goals()

    