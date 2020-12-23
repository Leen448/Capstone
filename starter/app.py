import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db, Actors, Movies
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app) 

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    #_____________Actor________________#

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors_list = Actors.query.all()
            if actors_list:
                return jsonify({'success': True, 
                'Actors': [{"id":actor.id, 'age': actor.age, 'name': actor.name} 
                            for actor in actors_list]}), 200
            else:
                return jsonify({'success': True, 'Actors': "None"}), 200
        except:
            return jsonify({'success': False, 'Actors': ""}), 404


    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(payload,id):
        try:
            get_actor = Actors.query.get(id)
            if get_actor:
                try:
                    get_body = request.get_json()
                    name = get_body.get('name',"")
                    age = get_body.get('age',"")
                    gender = get_body.get('gender',"")
                    
                    if name=="" and age=="" and gender==""  : abort(400)
                    if name:
                        get_actor.name = name
                    if age:
                        get_actor.age = age
                    if gender:
                        get_actor.gender = gender
                    get_actor.update()
                    return jsonify({
                        'success': True,
                        'actor': get_actor.name
                    }), 200
                except:
                    db.session.rollback()
                    abort(422)
            else:
                abort(404)
        except: 
            abort(422)
    	

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload,id):
        try:
            actor = Actors.query.get(id)
            if actor: 
                db.session.delete(actor)
                db.session.commit()
                return jsonify({
                        'success': True,
                        'actor':"Actor:"+ actor.name + " was successfuly deleted"
                    }), 200
            else: abort(404)        
        except:
            db.session.rollback()
            abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):
        try:
            if request.data is not None:
                json_body = request.get_json()

                name = json_body.get('name', "")
                age = json_body.get('age', "")
                gender = json_body.get('gender', "")

                if name=="" or age=="" or gender==""  : abort(400)

                actor_module = Actors(name=name, age=age, gender=gender)
                Actors.insert(actor_module)

                return jsonify({
                    'success': True,
                    'actor': actor_module.name
                }), 200
            else:
               abort(400)
        except:
             abort(422)

    #_____________Movies________________#

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies_list = Movies.query.all()
            if movies_list:
                return jsonify({'success': True, 
                'Movies': [{"id":movie.id, 'title': movie.title, 'releas date': movie.release_date} 
                            for movie in movies_list]}), 200
            else:
                return jsonify({'success': True, 'Movies': "None"}), 200
        except:
            return jsonify({'success': False, 'Movies': ""}), 404


    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload,id):
        try:
            movie_module = Movies.query.get(id)
            if movie_module:
                try:
                    # movie_module.delete()
                    db.session.delete(movie_module)
                    db.session.commit()
                    return jsonify({
                            'success': True,
                            'Movie':"Movie:"+ movie_module.title + " was successfuly deleted"
                        }), 200
                except: abort(422)
            else: abort(404)         
        except: abort(404)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(payload):
        try:
            if request.data:
                json_body = request.get_json()

                title = json_body.get('title', "" )
                release_date = json_body.get('release_date', "")
                 
                if title==""  or release_date=="":
                    abort(400)

                movie_module = Movies(title=title, release_date=release_date)
                Movies.insert(movie_module)

                return jsonify({
                    'success': True,
                    'Movie': movie_module.title
                }), 200
            else:
               abort(400)
        except:
             abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(payload,id):
            get_movie = Movies.query.get(id)
            if get_movie:
                try:
                    json_body = request.get_json()
                    title = json_body.get('title', "")
                    release_date = json_body.get('release_date', "")
                    
                    if title=="" and release_date=="" : abort(422)

                    if title:
                        get_movie.title = title
                    if release_date:
                        get_movie.release_date = release_date
                    get_movie.update()
                    return jsonify({
                        'success': True,
                        'movie': get_movie.title
                    }), 200
                except:
                    db.session.rollback()
                    abort(422) 
            else:
                abort(404)
    

    '''
    Error handlers
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False,
                        "error": 404,
                        "message": "Not found"}
                       ), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False,
                        "error": 422,
                        "message": "unprocessable"}
                       ), 422

    @app.errorhandler(400)
    def Bad_Request(error):
        return jsonify({"success": False,
                        "error": 400,
                        "message": "Bad Request"}
                       ), 400

    @app.errorhandler(500)
    def Internal_Server_Error(error):
        return jsonify(
            {"success": False,
             "error": 500,
             "message": "Internal Server Error"}
        ), 500


    @app.errorhandler(AuthError)
    def handle_auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            'message': e.error
        }), 401


    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
