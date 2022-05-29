from flask import Flask, jsonify

from utils import get_movie_by_title, get_movie_year_to_year, search_movie_by_rating, get_movies_by_genre

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/movie/<title>')
def movie_by_title(title):
    return get_movie_by_title(title)


@app.route('/movie/<int:year_1>/to/<int:year_2>')
def movie_year_to_year(year_1, year_2):
    return jsonify(get_movie_year_to_year(year_1, year_2))


@app.route('/rating/<category>')
def movie_by_rating(category):
    return jsonify(search_movie_by_rating(category))


@app.route('/genre/<genre>')
def movies_by_genre(genre):
    return jsonify(get_movies_by_genre(genre))


if __name__ == '__main__':
    app.run()
