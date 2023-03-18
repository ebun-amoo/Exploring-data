
from sqlalchemy import String, Integer, Float, Column
from sqlalchemy import select, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class PopCharts(Base):
    __tablename__ = "PopCharts"
    id = Column(Integer, primary_key=True)
    youtube_link = Column(String())
    name = Column(String())
    artist = Column(String())
    time_on_chart = Column(Integer)
    change = Column(Float)
    total_views = Column(Integer)
    num_likes = Column(Integer)
    duration = Column(Integer)
    views_this_week = Column(Integer)


class PopChartsExploration:
    def __init__(self, filename):
        self.engine = create_engine(f'sqlite:///{filename}', echo=False)
        Session = sessionmaker(self.engine)
        self.session = Session()
    
    def save(self):
        self.session.commit()
            
    def get_longest_song(self):
        result = (
            self.session.query(PopCharts)
            .order_by(PopCharts.duration.desc())
            .first())
            
        print(f'Found: {result.artist} - {result.name} {result.duration}')
        
    def count(self):
        result = (
            self.session.query(PopCharts)
            .count()
        )

        print(f"There are {result} songs in the Pop Charts database")
    
    def most_liked_song(self):
        result = (
            self.session.query(PopCharts)
            .order_by(PopCharts.num_likes.desc())
            .first()
        )

        print(f"The most liked song in the database is [{result.name}] by [{result.artist}]")
        
    def most_viewed_song(self):
        result = (
            self.session.query(PopCharts)
            .order_by(PopCharts.total_views.desc())
            .first()
        )

        print(f"The most viewed song in the database is [{result.name}] by [{result.artist}]")
        
    def trending_songs(self, n=10):
        subquery = (
            self.session.query(PopCharts.id, PopCharts.views_this_week,
                               PopCharts.total_views)
            .filter(PopCharts.views_this_week > 0)
            .subquery())
        
        trending_songs = (
            self.session.query(PopCharts)
            .join(subquery, PopCharts.id == subquery.c.id)
            .order_by(
                ((subquery.c.views_this_week / subquery.c.total_views - subquery.c.views_this_week)
                 .desc())
            )
            .limit(n)
            .all())
        print(f'Top {n} trending songs:')
        for song in trending_songs:
            print(f'- {song.name} - {song.artist}')
            
    def get_shortest_timechart(self):
        result = (
            self.session.query(PopCharts)
            .order_by(PopCharts.time_on_chart.asc())
            .first())
            
        print(f'\nFound: {result.artist} - {result.name} {result.time_on_chart} day(s)')
        

if __name__ == '__main__':
    popChartsExploration = PopChartsExploration('pop_charts_exploration.db')
    popChartsExploration.get_longest_song()
    popChartsExploration.count()
    popChartsExploration.most_liked_song()
    popChartsExploration.most_viewed_song()
    popChartsExploration.trending_songs()
    popChartsExploration.get_shortest_timechart()
    