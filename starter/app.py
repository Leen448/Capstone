import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import app, db,  Actors, Movies


def create_app(test_config=None):
    # create and configure the app
    
    app = Flask(__name__)
    db.init_app(app)
    CORS(app)
    

    #_____________Actor________________#

    @app.route('/actors')
    def get_actors():
        actors_list = Actors.query.all()
        return jsonify({'success': True, 'Actors': actors_list}), 200

    # @app.route('/actors', method=['PATCH'])
    # def edit_actors():
    # 	return

    # @app.route('/actors', method=['DELETE'])

    # def delete_actors():
    # 	return

    @app.route('/actors', methods=['POST'])
    def post_actors():
        try:
            if request.data is not None:
                json_body = request.get_json()
                name = json_body.get('name', None)
                age = json_body.get('age', None)
                gender = json_body.get('gender', None)

                actor_module = Actors(name=name, age=age, gender=gender)
                Actors.insert(actor_module)

                posted_actor = Actors.query.filter_by(
                    id=actor_module.id).first()

                return jsonify({
                    'success': True,
                    'actors': posted_actor.name
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'actors': "",
                    'error': "Bad Request"
                }), 400
        except BaseException:
            abort(422)

    #_____________Movies________________#

    @app.route('/movies')
    def get_movies():
        try:
            movies_list = Movies.query.all()
            return jsonify({
                'success': True,
                'Actors': movies_list
            }), 200
        except BaseException:
            returnabort(422)

    @app.route('/movies', methods=['DELETE'])
    def delete_movies():
    	return

    @app.route('/movies', methods=['POST'])

    def post_movies():
    	return

    @app.route('/movies', methods=['PATCH'])

    def edit_movies():
    	return


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

    return app

app = create_app()
db.init_app(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
