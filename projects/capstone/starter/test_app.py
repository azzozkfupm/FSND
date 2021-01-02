
import os
import unittest
import json
from app import create_app
from models import Actor,Movie,setup_db
from flask_sqlalchemy import SQLAlchemy

CASTING_ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZrbHpIQVNaenZSZHkwMDRYTFFXQSJ9.eyJpc3MiOiJodHRwczovL2F6ZWV6dWRhY2l0eS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZkMmQzZjBkMjE0YTIwMDc1MDY2M2I1IiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwLyIsImlhdCI6MTYwOTYxNzc4NSwiZXhwIjoxNjA5NjI0OTg1LCJhenAiOiJTS0drS2IzNk4yOTBzeWJPdUlkSmNzQW1KSjJzcFMyVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.i69gbwiVpjm6lKoS0q78ejGm8e_y4tGwanfQPnhijxRzhFM9d44VmEk_K8E6HWOYUk3_VsJ-DglDTl2KTCXUBgJvL-UjZaAbuikNqdK48aE6wJFi5ESgEK9sefiObKZyvZi_tZsp-WHZvDnoaVi9AKAxF0mhfRm3Fs0wDJ69a-Wxu2a7OShiRCtq_1UzfY-oomwhGLog7Ognqmwzja70EMBtCAhXQIjHit_dYX8hiHoafOhM5zAm6FoX9--IXgJOzkcdyIMh7yDH8gAm3V9EKp8z_BzW5x9-c6-453CySwmbWrm6sOeRwoRvJl-Hr2Hx66bXMoTRxcvvSO2fEJZp2A' 
CASTING_DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZrbHpIQVNaenZSZHkwMDRYTFFXQSJ9.eyJpc3MiOiJodHRwczovL2F6ZWV6dWRhY2l0eS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZlZTE0MTE4MTYzN2IwMDY4NWQxYjljIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwLyIsImlhdCI6MTYwOTYxNzk0MCwiZXhwIjoxNjA5NjI1MTQwLCJhenAiOiJTS0drS2IzNk4yOTBzeWJPdUlkSmNzQW1KSjJzcFMyVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.kfskqAftUmN72VPO_4VbaXqyAQvEfsd7vG9CBm7H_4uKpYdkuWbFWmBlyW12yyUILvJPpF7SZTLAxTDNQ-zIAZMz53SNqX83uMdZrFPOaQAlm5DXoIipbGu8ovoz3FPeQhhDcO3eR2EIXnlKxl189syQNUBToLfsLHu83nh8XAQU5X9z2w3J6e97ts8F5T6OMVG8P5sYgU9W0lIAzfBe4JrHZQks5Lb1dXwch00ZCA7TDVNczC_ApyeWqgKq9BF5kHp3OFrhEDGUS1D3-_HBLiZjcd1EomLQ3baebwiL9dmAgXumworDI0j1WZvZ3OJF8RUtANRFmDgumnwHV-Ippg'
EXECUTIVE_PRODUCER_TOKEN= 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZrbHpIQVNaenZSZHkwMDRYTFFXQSJ9.eyJpc3MiOiJodHRwczovL2F6ZWV6dWRhY2l0eS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZkMzllNzBmZjgzN2UwMDY4MTU0YzA5IiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwLyIsImlhdCI6MTYwOTYxODA2NywiZXhwIjoxNjA5NjI1MjY3LCJhenAiOiJTS0drS2IzNk4yOTBzeWJPdUlkSmNzQW1KSjJzcFMyVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.JE0CKM3O8pzaIN0gnPap2T25zD4J9BMev9oCm8bP1Rt-UQjW_zNOtvoZ8RDipYOUlLyPGudJXR9P8TAli09ce_4fXyxmTAzP4PwPPs3uZEKGQ-nX6U2cpvOoBBxg1xr5adSUrx38kt0O_jHMJrUTaZIV1QiCaApyObA2BDNDfidlZnWQQPKiqee8XJRCj2skK2yJTYGpVtHTTBsnwf-SAiQykuYVTv4yz9hlvxUzbTwlt484iCsQnbe5yF6Qk1Tn4u1nU2nfTu7OHey8PgyA7DwQ8_8Jl6hNcSPxVmiDIPheJH_gvg5oxw7MlVvFRHktWghqMGjMhufuC_gnE0oCzA'

class castingAgencyTesting(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        setup_db(self.app)        
       

    def tearDown(self):
        pass
    
    def test_get_actors(self):
        reponse=self.client().get('/actors',headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,200)
        self.assertTrue(json_data['actors'])

    def test_error_get_actors(self):
        reponse=self.client().get('/actors',headers='')
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,401)
        self.assertFalse(json_data['success'])
        self.assertFalse(len(json_data['actors']))

    def test_add_new_actor(self):
        new_actor = {
            name : 'John Dow',
            age : 55,
            gender:'male'
            }
        reponse=self.client().post('/actors',json=new_actor,headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,200)
        self.assertTrue(json_data['actor'])

    def test_error_add_new_actor(self):
        new_actor = {
            name : 'John Dow'
            }
        reponse=self.client().post('/actors',json=new_actor,headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,422)
        self.assertFalse(json_data['success'])        

    def test_update_existing_actor(self):
        new_actor = {
            id: 1,
            name : 'Lisa Dow',
            age : 55,
            gender:'female'
            }
        reponse=self.client().post('/actors/1',json=new_actor,headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,200)
        self.assertTrue(json_data['success'])        

    def test_error_update_existing_actor(self):
        new_actor = {
            id: 10,
            name : 'Lisa Dow',
            age : 55,
            gender:'female'
            }
        reponse=self.client().patch('/actors/10',json=new_actor,headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,422)
        self.assertFalse(json_data['success'])        
    
    def test_delete_existing_actor(self):

        reponse=self.client().delete('/actors/1',headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,200)
        self.assertTrue(json_data['success'])        
        
    def test_error_delete_existing_actor(self):
        reponse=self.client().delete('/actors/10',headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,422)
        self.assertFalse(json_data['success'])  

    def test_get_movies(self):
        reponse=self.client().get('/movies',headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,200)
        self.assertTrue(json_data['success'])

    def test_error_get_actors(self):
        reponse=self.client().get('/movies',headers='')
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,401)
        self.assertFalse(json_data['success'])
        self.assertFalse(len(json_data['actors']))

    def test_add_new_actor(self):
        new_actor = {
            title : 'Movie Night',
            release_date : '2021-01-02 22:42:19.590911'
            }
        reponse=self.client().post('/movies',json=new_actor,headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,200)
        self.assertTrue(json_data['success'])

    def test_error_add_new_actor(self):
        new_actor = {
            tite : 'Movie Night'
            }
        reponse=self.client().post('/actors',json=new_actor,headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,422)
        self.assertFalse(json_data['success'])        

    def test_update_existing_actor(self):
        new_movie = {
            id: 1,
            title : 'Movie Tomorroe' 
            }
        response=self.client().post('/movies/1',json=new_movie,headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertTrue(json_data['success'])        

    def test_error_update_existing_actor(self):
        new_movie = {
            id: 10,
            title : 'Movie Tomorroe' 
            }
        reponse=self.client().patch('/actors/10',json=new_movie,headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,422)
        self.assertFalse(json_data['success'])        
    
    def test_delete_existing_actor(self):

        response=self.client().delete('/movies/1',headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertTrue(json_data['success'])        
        
    def test_error_delete_existing_actor(self):
        reponse=self.client().delete('/movies/10',headers={"Authorization":"Bearer "+CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code,422)
        self.assertFalse(json_data['success'])  
