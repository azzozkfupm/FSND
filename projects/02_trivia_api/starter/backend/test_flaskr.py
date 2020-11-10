import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format('postgres:12345','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_retreiving_paginated_questions(self):
        res = self.client().get('/questions')
        paginated_questions = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(paginated_questions.get('success'))
        self.assertTrue(paginated_questions.get('questions'))
        self.assertEqual(len(paginated_questions.get('questions')),10)
        self.assertTrue(paginated_questions.get('total_questions'))
        self.assertTrue(paginated_questions.get('categories'))

    def test_404_not_retreiving_paginated_questions(self):
        res = self.client().get('/questions?page=8')
        paginated_questions = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertFalse(paginated_questions.get('success'))
        self.assertEqual(paginated_questions.get('message'),"not found")

    def test_creating_question(self):
        total_question = len(Question.query.all())
        question = {
            'question':'This is test question',
            'answer':'this is test answer',
            'category':2,
            'difficulty':2
            }

        res = self.client().post('/questions',json=question)
        data = json.loads(res.data)
        total_question1 = len(Question.query.all())

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertEqual(total_question + 1 ,total_question1)

    def test_422_not_creating_question(self):
     
        question = {
            'question':'This is test question',
            'answer':'this is test answer',
            }

        res = self.client().post('/questions',json=question)
        data = json.loads(res.data)
        

        self.assertEqual(res.status_code,422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] ,'unable to process')

    def test_deleting_question(self):

        question = Question(question='this to be deleted',answer= 'deleted answer',difficulty=3,category=3)
        question.insert()
        q_id = question.id
        res = self.client().delete(f'/questions/{q_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertEqual(data['delete'],str(q_id))

    def test_422_not_deleting_question(self):

        res = self.client().delete('/questions/test')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'unable to process')

    def test_question_by_category(self):
        category = 2
        res = self.client().get(f'/categories/{category}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'],2)

    def test_404_question_by_category(self):
        category = 'windows'
        res = self.client().get(f'/categories/{category}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'not found')

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])
 
    def test_404_get_categories(self):
        res = self.client().get('/categories/200')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'not found')

    def test_search_question(self):
        search_term = {'searchTerm':'country'}
        
        res = self.client().post('/questions/search',json= search_term) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('questions'))
        self.assertTrue(data.get('total_questions'))
      
    def test_404_search_question(self):
        search_term = {'searchTerm':''}
        
        res = self.client().post('/questions/search',json= search_term) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertFalse(data.get('success'))
        self.assertTrue(data.get('message'),'not found')

    def test_get_quizzes(self):
        category={'previous_questions':[],'quiz_category':{'type':'History','id':4}}
        res = self.client().post('/quizzes',json=category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('question'))
  

    def test_422_get_quizzes(self):
        category={'quiz_category':{'type':'History','id':4}}
        res = self.client().post('/quizzes',json=category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertFalse(data.get('success'))
        self.assertEqual(data.get('message'),'unable to process')
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
