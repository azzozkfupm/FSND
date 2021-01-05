
import os
import unittest
import json
from app import create_app
from models import Actor, Movie, setup_db
from flask_sqlalchemy import SQLAlchemy

CASTING_ASSISTANT_TOKEN = '''eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZr
                            bHpIQVNaenZSZHkwMDRYTFFXQSJ9.eyJpc3MiOiJodHRwczov
                            L2F6ZWV6dWRhY2l0eS51cy5hdXRoMC5jb20vIiwic3ViIjoiY
                            XV0aDB8NWZkMmQzZjBkMjE0YTIwMDc1MDY2M2I1IiwiYXVkIj
                            oiaHR0cDovL2xvY2FsaG9zdDo4MDgwLyIsImlhdCI6MTYwOTg
                            3NTA2NCwiZXhwIjoxNjA5ODgyMjY0LCJhenAiOiJTS0drS2Iz
                            Nk4yOTBzeWJPdUlkSmNzQW1KSjJzcFMyVCIsInNjb3BlIjoiI
                            iwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3
                            ZpZXMiXX0.XpQqFterBSQr_sJYN3vkbWYrjEzobtLDGgy0Z5w
                            bY6zzVMSXjwBn_Y3zT1eBXJI1dufb6_xCMc35QyHJ4MWPkHnn
                            rCtoWvkrmd8gWAvciF6EnGnAFks1K2zf5P-wnLA7ctl3l6BJ3
                            JNyqvUeTNS6xTDLXYSud_77ZzBMeRXfuBoUVL-mKU0NkvxTg8
                            sWslbZBGATgGXj3K9xPELXIBQo6MZwKKFL1rCMwKv6SDqEKAH
                            cYdWs5H3mnNYWBGgVvXaU_7GiKJrfa8OtF9BZM4irsTrTh8DV
                            5M8N2UfiT-CrpBrjEiqdnfyhpd-p8MbTw5Z5cYKXmtAaFcqlR
                            VeF77M7GQ'''
CASTING_DIRECTOR_TOKEN = '''eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZrb
                            HpIQVNaenZSZHkwMDRYTFFXQSJ9.eyJpc3MiOiJodHRwczovL
                            2F6ZWV6dWRhY2l0eS51cy5hdXRoMC5jb20vIiwic3ViIjoiYX
                            V0aDB8NWZlZTE0MTE4MTYzN2IwMDY4NWQxYjljIiwiYXVkIjo
                            iaHR0cDovL2xvY2FsaG9zdDo4MDgwLyIsImlhdCI6MTYwOTg3
                            NTMwNSwiZXhwIjoxNjA5ODgyNTA1LCJhenAiOiJTS0drS2IzN
                            k4yOTBzeWJPdUlkSmNzQW1KSjJzcFMyVCIsInNjb3BlIjoiIi
                            wicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmF
                            jdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBh
                            dGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.e20PB_fOW8-XlR
                            aNXxyTYakvojSMDVMLIYyHLe00oK_x0C76VZrxvmQdZNZ1nTl
                            0B2hi3DMQvVkBgWLEwZc0b5_ftQBXpXSKYwzYA2To_d11Gt2u
                            9dFe7IPd7rBftCYYXcL_Mm8Q-MR7oQ68Wneo03SfFz5kPZxze
                            YNP1nexvtABiA3oGclKYwjnLnkyc6d7B6j8qlh1Ye8BBAc8RS
                            jNF_QYeN9potcNV1UAoNpI2QB-5zdSOPSqRDmpeJWuy3NDi3T
                            Hn5RolLTQKhq7OwRiFu1rGzx6yOnYe6IfiVeQtScfTzBFy7_G
                            qMFl-occlkxG8XnRV2ATQ-2VgwR_ZAntzw'''
EXECUTIVE_PRODUCER_TOKEN = '''eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZ
                            rbHpIQVNaenZSZHkwMDRYTFFXQSJ9.eyJpc3MiOiJodHRwczo
                            vL2F6ZWV6dWRhY2l0eS51cy5hdXRoMC5jb20vIiwic3ViIjoi
                            YXV0aDB8NWZkMzllNzBmZjgzN2UwMDY4MTU0YzA5IiwiYXVkI
                            joiaHR0cDovL2xvY2FsaG9zdDo4MDgwLyIsImlhdCI6MTYwOT
                            g3NTQ5OCwiZXhwIjoxNjA5ODgyNjk4LCJhenAiOiJTS0drS2I
                            zNk4yOTBzeWJPdUlkSmNzQW1KSjJzcFMyVCIsInNjb3BlIjoi
                            IiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZ
                            XRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLC
                            JwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3R
                            vciIsInBvc3Q6bW92aWUiXX0.scNP88zpZvOcR1tjNJYp_wqG
                            N4A-O6wAj2-tLQdQSXdtyIrqXRaIwcAoXxVwjXv59te2407Vv
                            0oW2_6pYxUwjmv9zYp8V-sLQFZhG-PDPBdjTlXjBKZKQn1yIM
                            B1DhuISHN8jyL7t0BakUkbn-qjQF2VxaOjul7bprqz21TLj5R
                            xTMwju5D-ktYqM2xbyKpEKgAMlezkYrybHiL7TXnk_r4qA0Rj
                            048--LY2IV8HhvXgwEi8dpJ88XqVIwBKAclUiExw18FOBmqkt
                            kackfw_Kc3JMtT4xQ8ZjBm5bDE-N_CMQCbhUdH-ocJlPFsLNc
                            8msaqck0JAursYQtXpFzKk4A'''


class castingAgencyTesting(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        setup_db(self.app)

    def tearDown(self):
        pass

    def test_get_actors(self):
        reponse = self.client().get('/actors', headers={
                                "Authorization": "Bearer " +
                                CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 200)
        self.assertTrue(json_data['actors'])

    def test_error_get_actors(self):
        reponse = self.client().get('/actors', headers='')
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 401)
        self.assertFalse(json_data['success'])
        self.assertFalse(len(json_data['actors']))

    def test_add_new_actor(self):
        new_actor = {
            name: 'John Dow',
            age: 55,
            gender: 'male'
            }
        reponse = self.client().post(
                                    '/actors',
                                    json=new_actor,
                                    headers={
                                        "Authorization": "Bearer "
                                        + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 200)
        self.assertTrue(json_data['actor'])

    def test_error_add_new_actor(self):
        new_actor = {
            name: 'John Dow'
            }
        reponse = self.client().post(
                                    '/actors',
                                    json=new_actor,
                                    headers={
                                        "Authorization": "Bearer " +
                                        CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 422)
        self.assertFalse(json_data['success'])

    def test_update_existing_actor(self):
        new_actor = {
            id: 1,
            name: 'Lisa Dow',
            age: 55,
            gender: 'female'
            }
        reponse = self.client().post(
                                    '/actors/1',
                                    json=new_actor,
                                    headers={
                                        "Authorization": "Bearer "
                                        + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 200)
        self.assertTrue(json_data['success'])

    def test_error_update_existing_actor(self):
        new_actor = {
            id: 10,
            name: 'Lisa Dow',
            age: 55,
            gender: 'female'
            }
        reponse = self.client().patch(
                                    '/actors/10',
                                    json=new_actor,
                                    headers={
                                        "Authorization": "Bearer "
                                        + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 422)
        self.assertFalse(json_data['success'])

    def test_delete_existing_actor(self):

        reponse = self.client().delete(
                                    '/actors/1',
                                    headers={
                                        "Authorization": "Bearer "
                                        + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 200)
        self.assertTrue(json_data['success'])

    def test_error_delete_existing_actor(self):
        reponse = self.client().delete(
                                    '/actors/10',
                                    headers={
                                        "Authorization": "Bearer "
                                        + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 422)
        self.assertFalse(json_data['success'])

    def test_get_movies(self):
        reponse = self.client().get(
                                '/movies',
                                headers={
                                    "Authorization": "Bearer "
                                    + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 200)
        self.assertTrue(json_data['success'])

    def test_error_get_actors(self):
        reponse = self.client().get('/movies', headers='')
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 401)
        self.assertFalse(json_data['success'])
        self.assertFalse(len(json_data['actors']))

    def test_add_new_actor(self):
        new_actor = {
            title: 'Movie Night',
            release_date: '2021-01-02 22:42:19.590911'
            }
        reponse = self.client().post(
                                    '/movies',
                                    json=new_actor,
                                    headers={
                                        "Authorization": "Bearer "
                                        + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 200)
        self.assertTrue(json_data['success'])

    def test_error_add_new_actor(self):
        new_actor = {
            tite: 'Movie Night'
            }
        reponse = self.client().post(
                                    '/actors',
                                    json=new_actor,
                                    headers={
                                        "Authorization": "Bearer "
                                        + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 422)
        self.assertFalse(json_data['success'])

    def test_update_existing_actor(self):
        new_movie = {
            id: 1,
            title: 'Movie Tomorroe'
            }
        response = self.client().post(
                                    '/movies/1',
                                    json=new_movie,
                                    headers={
                                        "Authorization": "Bearer "
                                        + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_data['success'])

    def test_error_update_existing_actor(self):
        new_movie = {
            id: 10,
            title: 'Movie Tomorroe'
            }
        reponse = self.client().patch(
                                    '/actors/10',
                                    json=new_movie,
                                    headers={
                                        "Authorization": "Bearer "
                                        + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 422)
        self.assertFalse(json_data['success'])

    def test_delete_existing_actor(self):

        response = self.client().delete(
                                    '/movies/1',
                                    headers={
                                        "Authorization": "Bearer "
                                        + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_data['success'])

    def test_error_delete_existing_actor(self):
        reponse = self.client().delete(
                                    '/movies/10',
                                    headers={
                                        "Authorization": "Bearer "
                                        + CASTING_ASSISTANT_TOKEN})
        json_data = json.loads(reponse.data)
        self.assertEqual(reponse.status_code, 422)
        self.assertFalse(json_data['success'])
