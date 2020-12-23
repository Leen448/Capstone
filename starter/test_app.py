import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app , create_app
from models import setup_db, db, Actors, Movies
import random


casting_assistant_token=(os.environ.get('casting_assistant_token'))
casting_director_token=(os.environ.get('casting_director_token'))
executive_producer_token=(os.environ.get('executive_producer_token'))

# casting_assistant_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFPYXJMWTlJcVQ1OUFiQ0xBeWRYOCJ9.eyJpc3MiOiJodHRwczovL3RhMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZjNjNlY2MzYjc2MTgwMDY4ZGYyMTZhIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTYwODY1ODk3OSwiZXhwIjoxNjA4NzQ1Mzc5LCJhenAiOiJZTGVvMU5XeEVpM3lMcHlaZDBhYmkzczZiZzFTNkRWNCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.wAyCoSB5D0i3JOAvJhDXfYw_xND1ts31ABRImhuKZ29SaxrqhRKjGpSXo077iBeOW8yftomGX9bcmq4jLr5yThib6447kyEu0O-Kj2x_q5HPxPOxPdLtPmEs4s1urY2aWZi_FO9AwIV4hXx8234N5jMCuCoqsIPQ3o_0RoAN4lvloLoj02gdlz6aOkOSlk6oWZ81TUO4uyndEFQw7Ee74P17lgdj2kosV7ZqHO21purvprPaKWgV68vJlngmIRlqjo9QjPnDAgM-5e7mPEAxyizJNL7gY-WdsXazm7kJYWbTTxpTiQJBn7FN5TmYWWTmay9FQqqSF2djOx4llC9rsg'
# casting_director_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFPYXJMWTlJcVQ1OUFiQ0xBeWRYOCJ9.eyJpc3MiOiJodHRwczovL3RhMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZlMGU1MTU1Njk2YWUwMDcxMmUxNGQ2IiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTYwODY2MDM3MiwiZXhwIjoxNjA4NzQ2NzcyLCJhenAiOiJZTGVvMU5XeEVpM3lMcHlaZDBhYmkzczZiZzFTNkRWNCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.dodgCSLy0Dp9Lz2tLt5icagT0IDxhyOVdOQCHNzVgaHTKzRpOtz9btVMdPU2Qal6VaNCNGOgu4baxjZR2hVWzuFBOY3DZK00b8lh2zA5pXYcuZyBrIbzV3YGpEeuYyCXU30tv7yiouHvxLsNz1MGe0nH7GksbBgKoeGYXkrEUQ44AGPzU0zWepd8x4iRWUpzvVm8OTpW8HiVgHTdfJFZTK1gPXGXz7v6FhneWChHBR_HDHAFW5xsRB_SQltbc3eMgb2MY15FQ1fJKwQJuoTlEL5Xb9MHnR1AK62-n_R0cbJSRSTeoFqlBTRXClvsW4x_ZxjI-0Kxy_83KBeS2qp3TA'
# executive_director_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFPYXJMWTlJcVQ1OUFiQ0xBeWRYOCJ9.eyJpc3MiOiJodHRwczovL3RhMC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTM3OTkwODg1MDI4MjI3NDY2NzEiLCJhdWQiOlsiY2FzdGluZ2FnZW5jeSIsImh0dHBzOi8vdGEwLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDg2NjAwOTcsImV4cCI6MTYwODc0NjQ5NywiYXpwIjoiWUxlbzFOV3hFaTN5THB5WmQwYWJpM3M2YmcxUzZEVjQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.wsBSPDTk0cIoKO49ttd2o_t9F9fwLv9scx5yAtfRHv703cLmpb4Av1R3Eo3N_hxZW1f0vRh3vFHcttfrqTQt-ZR-dJEHYu8gXhD3rpWzPJnp3k3rb-tX8MU6vSpHAHYSReN0Vjt9Xr3qYuq-pBqJQF_iVhnMaSFBiwCPhxOIKqBSfZkGi9zUINk8rCuVeAhS48yM1F2x22piWTs9_rxGWZN2PzQD3vLMgnk2fg9gBFtCEHxnvQQOI8Zhd99DAK60TrJn71OO3nPz4BDQLqrpM1l3QExRzP3I8sq29R6IEd4gXxkcELS0q7_VHxXyqlYxo-_YZYabucL010BcjTzk2Q'



database_path =  (os.environ.get('DATABASE_URL_TEST'))

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        self.casting_assistant_token=casting_assistant_token
        self.casting_director_token=casting_director_token
        self.executive_producer_token=executive_producer_token
        setup_db(self.app, self.database_path)

    def tearDown(self):
        # '''Executed after reach test'''
        pass


# # post
    '''post actor'''
    def test_success_post_new_actor(self):
        response_object = self.client().post('/actors',
            headers={'Authorization': 'Bearer {}'.format( self.executive_producer_token)},
                                                json={
                                                    'name': 'test1',
                                                    'age': '45',
                                                    'gender': 'male'
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['actor'])
        
    '''post actor 422'''
    def test_422_unprocessable_post_actor(self):

        response_object = self.client().post('/actors',
             headers={'Authorization': 'Bearer {}'.format( self.executive_producer_token)},
                                                json={
                                                    'name':''
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 422)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'unprocessable')      


    '''post moive'''
    def test_success_post_new_movie(self):
        response_object = self.client().post('/movies',
            headers={'Authorization': 'Bearer {}'.format( self.executive_producer_token)},
                                                json={
                                                    'title': 'test1',
                                                    'release_date' : '12/12/2020'
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['Movie'])    

    '''post moive 422'''
    def test_422_unprocessable_post_movie(self):

        response_object = self.client().post('/movies',
             headers={'Authorization': 'Bearer {}'.format( self.executive_producer_token)},
                                                json={
                                                    'title': '',
                                                    'release_date' : '12/12/2020'
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
            headers={'Authorization': 'Bearer {}'.format( self.casting_assistant_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['Actors'])

    '''
    test_get_Movies
    '''
    
    def test_get_Movies(self):
        response_object = self.client().get('/movies',
            headers={'Authorization': 'Bearer {}'.format( self.casting_assistant_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['Movies'])


# bathc
    '''batch movie '''
    def test__edit_movie(self):
        random_id = random.choice([movie.id for movie in Movies.query.all()])
        response_object = self.client().patch('/movies/'+str(random_id),    
            headers={'Authorization': 'Bearer {}'.format( self.casting_director_token)},
                                                json={
                                                    'title': 'good feel'
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['movie']) 

    '''batch movie 422'''
    def test_422_unprocessable_edit_movie(self):
        random_id = random.choice([movie.id for movie in Movies.query.all()])
        response_object = self.client().patch('/movies/'+str(random_id),   
            headers={'Authorization': 'Bearer {}'.format( self.casting_director_token)},
                                                json={
                                                    'title': ''
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 422)
        self.assertEqual(response_data['success'], False)
      

    '''batch actor '''    
    def test_edit_actor(self):
        random_id = random.choice([actor.id for actor in Actors.query.all()])
        response_object = self.client().patch('/actors/'+str(random_id),
             headers={'Authorization': 'Bearer {}'.format( self.casting_director_token)},
                                                json={
                                                    'name':'leen'
                                                    })
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['actor']) 

    '''batch actor 422'''  
    def test_422_unprocessable_edit_actor(self):
        response_object = self.client().patch('/actors/1',
             headers={'Authorization': 'Bearer {}'.format( self.casting_director_token)},
                                                json={
                                                    'name':''
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
        response_object = self.client().delete('/actors/'+str(random_id),     
            headers={'Authorization': 'Bearer {}'.format( self.executive_producer_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertTrue(response_data['actor'])


    '''
        A request to delete a question with a 
        non-existent id should return a 400 status code
    '''

    def test_404_delete_actor(self):
        response_object = self.client().delete('/actors/300000',    
             headers={'Authorization': 'Bearer {}'.format( self.executive_producer_token)})
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
        response_object = self.client().delete('movies/'+str(random_id),
             headers={'Authorization': 'Bearer {}'.format( self.executive_producer_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 200)
        self.assertTrue(response_data['Movie'])


    '''
        A request to delete a question with a 
        non-existent id should return a 400 status code
    '''

    def test_400_delete_movie(self):
        response_object = self.client().delete('/movies/300000',  
           headers={'Authorization': 'Bearer {}'.format( self.executive_producer_token)})
        response_data = json.loads(response_object.get_data())

        self.assertEqual(response_object.status_code, 404)
        self.assertEqual(response_data['success'], False)
        self.assertEqual(response_data['message'], 'Not found')    


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
