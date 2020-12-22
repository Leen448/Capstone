import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import setup_db, db, Actors, Movies
import random



casting_assistant_token  = os.environ.get('casting_assistant_token')
casting_director_token   = os.environ.get('casting_director_token')
executive_producer_token = os.environ.get('executive_producer_token')
database_path_test = os.environ.get('SQLALCHEMY_DATABASE_TEST_URI')

class CastingAgecnyTestCase(unittest.TestCase):

    def setUp(self):
        # """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = database_path_test
        self.executive_producer_token=executive_producer_token
        self.casting_director_token=casting_director_token
        self.casting_assistant_token=casting_assistant_token
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
            

    def tearDown(self):
        # """Executed after reach test"""
        pass


# # post
    '''post actor'''
    def test_success_post_new_actor(self):
        response_object = self.client().post('/actors',
            headers={"Authorization": "Bearer {}".format(self.executive_producer_token)},
                                                json={
                                                    "name": "test1",
                                                    "age": "45",
                                                    "gender": "male"
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['actor'])
        
    '''post actor 422'''
    def test_422_unprocessable_post_actor(self):

        response_object = self.client().post('/actors',
             headers={"Authorization": "Bearer {}".format(self.executive_producer_token)},
                                                json={
                                                    "name":""
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 422)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'unprocessable')      


    '''post moive'''
    def test_success_post_new_movie(self):
        response_object = self.client().post('/movies',
            headers={"Authorization": "Bearer {}".format(self.executive_producer_token)},
                                                json={
                                                    "title": "test1",
                                                    "release_date" : "12/12/2020"
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['Movie'])    

    '''post moive 422'''
    def test_422_unprocessable_post_movie(self):

        response_object = self.client().post('/movies',
             headers={"Authorization": "Bearer {}".format(self.executive_producer_token)},
                                                json={
                                                    "title": "",
                                                    "release_date" : "12/12/2020"
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 422)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'unprocessable')
  

# get
    '''
    test_get_Actors
    '''
    def test_get_actors(self):
        response_object = self.client().get('/actors',
            headers={"Authorization": "Bearer {}".format(self.casting_assistant_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['Actors'])

    '''
    test_get_Movies
    '''
    
    def test_get_Movies(self):
        response_object = self.client().get('/movies',
            headers={"Authorization": "Bearer {}".format(self.casting_assistant_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['Movies'])


# bathc
    '''batch movie '''
    def test__edit_movie(self):
        random_id = random.choice([movie.id for movie in Movies.query.all()])
        response_object = self.client().patch('/movies/'+str(random_id),    
            headers={"Authorization": "Bearer {}".format(self.casting_director_token)},
                                                json={
                                                    "title": "good feel"
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['movie']) 

    '''batch movie 422'''
    def test_422_unprocessable_edit_movie(self):
        random_id = random.choice([movie.id for movie in Movies.query.all()])
        response_object = self.client().patch('/movies/'+str(random_id),   
            headers={"Authorization": "Bearer {}".format(self.casting_director_token)},
                                                json={
                                                    "title": ""
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 422)
        self.assertEqual(response_data['success'], False)
      

    '''batch actor '''    
    def test_edit_actor(self):
        random_id = random.choice([actor.id for actor in Actors.query.all()])
        response_object = self.client().patch('/actors/'+str(random_id),
             headers={"Authorization": "Bearer {}".format(self.casting_director_token)},
                                                json={
                                                    "name":"leen"
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['actor']) 

    '''batch actor 422'''  
    def test_422_unprocessable_edit_actor(self):
        response_object = self.client().patch('/actors/1',
             headers={"Authorization": "Bearer {}".format(self.casting_director_token)},
                                                json={
                                                    "name":""
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 422)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'unprocessable')  

    '''delete'''

    '''
        A request to delete a given question with the specified id should return a 200
        status code and should delete the question from the database
    '''

    def test_success_delete_actor(self):
        random_id = random.choice([actor.id for actor in Actors.query.all()])
        response_object = self.client().delete("/actors/"+str(random_id),     
            headers={"Authorization": "Bearer {}".format(self.executive_producer_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data["actor"])


    '''
        A request to delete a question with a 
        non-existent id should return a 400 status code
    '''

    def test_400_delete_actor(self):
        response_object = self.client().delete("/actors/300000",    
             headers={"Authorization": "Bearer {}".format(self.executive_producer_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Not found')


    '''
        A request to delete a given question with the specified id should return a 200
        status code and should delete the question from the database
    '''

    def test_success_delete_movie(self):
        random_id = random.choice([movie.id for movie in Movies.query.all()])
        response_object = self.client().delete("movies/"+str(random_id),
             headers={"Authorization": "Bearer {}".format(self.executive_producer_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertTrue(response_data['Movie'])


    '''
        A request to delete a question with a 
        non-existent id should return a 400 status code
    '''

    def test_400_delete_movie(self):
        response_object = self.client().delete("/movies/300000",  
           headers={"Authorization": "Bearer {}".format(self.executive_producer_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Not found')    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
