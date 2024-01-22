from flask import Flask, jsonify, render_template
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String

Base = declarative_base()


class Actor(Base):
    __tablename__ = 'top_actors'
    nconst = Column(String, primary_key=True)
    primaryName = Column(String)
    FilmCount = Column(Integer)


# Define the Movie table
class Movie(Base):
    __tablename__ = 'top_movies'
    genres = Column(String, primary_key=True)
    primaryTitle = Column(String)
    AverageRating = Column(Integer)
    MovieCount = Column(Integer)

app = Flask(__name__)

# Configure the database connection
database_url = 'sqlite:///output/imdb_database.db'
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)

# Function to convert SQLAlchemy object to dictionary
def to_dict(obj):
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}

# Function to get top actors from the database
def get_top_actors():
    session = Session()
    top_actors = session.query(Actor).order_by(Actor.FilmCount.desc()).all()
    top_actors_dict = [to_dict(actor) for actor in top_actors]
    session.close()
    return top_actors_dict

# Function to get top movies from the database
def get_top_movies():
    session = Session()
    top_movies = session.query(Movie).order_by(Movie.AverageRating.desc()).all()
    top_movies_dict = [to_dict(movie) for movie in top_movies]
    session.close()
    return top_movies_dict

# Define routes to serve the data
@app.route('/api/top_actors', methods=['GET'])
def top_actors_route():
    top_actors = get_top_actors()
    return jsonify(top_actors)

@app.route('/api/top_movies', methods=['GET'])
def top_movies_route():
    top_movies = get_top_movies()
    return jsonify(top_movies)


@app.route('/')
def index():
    session = Session()

    # Get top actors
    top_actors = session.query(Actor).order_by(Actor.FilmCount.desc()).all()

    # Get top movies
    top_movies = session.query(Movie).order_by(Movie.AverageRating.desc()).all()

    session.close()

    # Render the HTML template with the top actors and top movies data
    return render_template('index.html', top_actors=top_actors, top_movies=top_movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
