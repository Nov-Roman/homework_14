import json
import sqlite3
from collections import Counter


class DatabaseConnect:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()


def get_movie_by_title(title):
    """
    Поиск по названию фильма
    """
    database_connect = DatabaseConnect('netflix.db')
    sqlite_query = f"""
                    select title, country, release_year, listed_in, description
                    from netflix
                    where title like '%{title}%'
                    order by release_year desc 
    """
    database_connect.cur.execute(sqlite_query)
    result = database_connect.cur.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def get_movie_year_to_year(year_1, year_2):
    """
    Поиск по диапазону лет выпуска
    """
    database_connect = DatabaseConnect('netflix.db')
    sqlite_query = f"""
                    select title, release_year
                    from netflix
                    where release_year between {year_1} and {year_2}
                    limit 100
    """
    database_connect.cur.execute(sqlite_query)
    result = database_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "release_year": movie[1]})
    return result_list


def search_movie_by_rating(rating):
    """
    Поиск по рейтингу.
    - G — нет возрастных ограничений.
    - PG — желательно присутствие родителей.
    - PG-13 — для детей от 13 лет в присутствии родителей.
    - R — дети до 16 лет допускаются на сеанс только в присутствии родителей.
    - NC-17 — дети до 17 лет не допускаются.
    """
    database_connect = DatabaseConnect('netflix.db')
    ratings = {
        "children": "'G'",
        "family": "'G' , 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    sqlite_query = f"""
                    select title, rating, description
                    from netflix
                    where rating in ({ratings[rating]})
    """
    database_connect.cur.execute(sqlite_query)
    result = database_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "rating": movie[1],
                            "description": movie[2]})
    return result_list


def get_movies_by_genre(genre):
    """
    Получает название жанра в качестве аргумента и возвращает 10 самых свежих фильмов.
    """
    database_connect = DatabaseConnect('netflix.db')
    sqlite_query = f"""
                    select title, description
                    from netflix
                    where listed_in like '%{genre}%'
                    order by release_year desc 
                    limit 10
    """
    database_connect.cur.execute(sqlite_query)
    result = database_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "description": movie[1]})
    return result_list


def get_cast_actors(actor_1, actor_2):
    """
    Получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех,
    кто играет с ними в паре больше 2 раз
    """
    database_connect = DatabaseConnect('netflix.db')
    sqlite_query = f"""
                    select `cast`
                    from netflix
                    where `cast` like '%{actor_1}%' and `cast` like '%{actor_2}%'
    """
    database_connect.cur.execute(sqlite_query)
    result = database_connect.cur.fetchall()
    actors = []
    for cast in result:
        actors.extend(cast[0].split(', '))
    counter = Counter(actors)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor_1, actor_2] and count > 2:
            result_list.append(actor)
    return result_list


def get_movie_by_type(movie_type, release_year, genre):
    """
    Тип картины (фильм или сериал), год выпуска и ее жанр,
    на выходе список названий картин с их описаниями
    """
    database_connect = DatabaseConnect('netflix.db')
    sqlite_query = f"""
                    select title, description
                    from netflix
                    where `type` = '{movie_type}'
                    and release_year = {release_year}
                    and listed_in like '%{genre}%'
    """
    database_connect.cur.execute(sqlite_query)
    result = database_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({'title': movie[0],
                            'description': movie[1]})
    return json.dumps(result_list)
