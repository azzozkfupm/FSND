import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db_drop_create_all, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
              'Access-Control-Allow-Headers',
              'Content-Type, Authorization , true')
        response.headers.add(
              'Access-Control-Allow-Methods',
              'GET, PATCH, POST, DELETE, OPTIONS')

        return response

    @app.route("/", methods=['GET'])
    def index():
        return jsonify({
            'message': 'This is the homepage of the casting agency'
        })

    @app.route('/actors')
    @requires_auth('get:actors')
    def all_actors(token):
        try:
            all_actors = Actor.query.all()
            actors = [actor.format() for actor in all_actors]
        except Exception:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'actors': actors
            }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def post_new_actor(token):
        user_input = request.get_json()
        actor = Actor(
            name=user_input['name'],
            age=user_input['age'],
            gender=user_input['gender']
           )

        try:
            actor.insert()
        except Exception:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def patch_actor(token, id):
        user_input = request.get_json()
        try:
            actor = Actor.query.get(id)
            actor.name = user_input['name']
            actor.age = user_input['age']
            actor.gender = user_input['gender']
            actor.update()
        except Exception:
            abort(422)

        else:
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200

    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(token, id):
        try:
            actor = Actor.query.get(id)
            actor.delete()
        except Exception:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'deleted_actor': id
            }), 200

    @app.route('/movies')
    @requires_auth('get:movies')
    def all_movies(token):
        try:
            all_movies = Movie.query.all()
            movies = [movie.format() for movie in all_movies]
        except Exception:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'movies': movies
            }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def post_new_movie(token):
        user_input = request.get_json()
        movie = Movie(
            title=user_input['title'],
            release_date=user_input['release_date'])

        try:
            movie.insert()
        except Exception:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def patch_movie(token, id):

        user_input = request.get_json()
        try:
            movie = Movie.query.get(id)
            movie.title = user_input['title']
            movie.release_date = user_input['release_date']
            movie.update()
        except Exception:
            abort(422)

        else:
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

    @app.route('/movie/<id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(token, id):
        try:
            movie = Movie.query.get(id)
            movie.delete()
        except Exception:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'deleted_movie': id
            }), 200

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unable to process request'
          })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
          })

    @app.errorhandler(401)
    def unotherized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'unotherized'
          })

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'page not found'
          })

    @app.errorhandler(AuthError)
    def autherror(err):
        return jsonify({
              'success': False,
              'error': err.status_code,
              'message': err.error
          })
    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
