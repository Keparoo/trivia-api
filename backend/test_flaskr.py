#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

#----------------------------------------------------------------------------#
# Setup Trivia Tests
#----------------------------------------------------------------------------#
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','password','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # new question for testing create question
        self.test_question = {
          'question': 'Which particle binds quarks in a nucleus',
          'answer': 'gluon',
          'difficulty': 4,
          'category': '1'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

#----------------------------------------------------------------------------#
# API Endpoint tests
#----------------------------------------------------------------------------#
    def test_get_categories(self):
      res = self.client().get('/categories')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_non_existing_category(self):
      res = self.client().get('/categories/1000')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 404)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'resource not found')

    def test_get_paginated_questions(self):
      res = self.client().get('/questions')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['total_questions'])
      self.assertTrue(len(data['questions']))
      self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_beyond_valid_page(self):
      res = self.client().get('/questions?page=1000')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 404)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_by_category(self):
      res = self.client().get('/categories/1/questions')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['total_questions'])
      self.assertTrue(len(data['questions']))
      self.assertEqual(data['current_category'], "Science")

    def test_get_questions_by_category_fail(self):
      res = self.client().get('/categories/100/questions')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 400)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'bad request')

    def test_create_question(self):
      '''Tests create_question success'''

      num_questions_before = Question.query.all()

      res = self.client().post('/questions', json=self.test_question)
      data = json.loads(res.data)

      num_questions_after = Question.query.all()
      
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(len(num_questions_after) - len(num_questions_before) == 1)

    def test_422_create_question_fails(self):
      '''Tests create_question failure sends 422'''

      num_questions_before = Question.query.all()

      res = self.client().post('/questions', json={})
      data = json.loads(res.data)

      num_questions_after = Question.query.all()

      self.assertEqual(res.status_code, 422)
      self.assertEqual(data['success'], False)

      self.assertTrue(len(num_questions_after) == len(num_questions_before))

    def test_delete_question(self):
      '''Tests delete_question success'''

      # create a question to delete
      question = Question(question=self.test_question['question'], answer=self.test_question['answer'], category=self.test_question['category'], difficulty=self.test_question['difficulty'])

      question.insert()
      question_id = question.id

      num_questions_before = Question.query.all()

      res = self.client().delete(f'/questions/{question_id}')
      data = json.loads(res.data)

      num_questions_after = Question.query.all()

      question = Question.query.filter(Question.id == 1).one_or_none()

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(len(num_questions_before) - len(num_questions_after) == 1)
      self.assertEqual(data['deleted'], question_id)
      self.assertEqual(question, None)

    def test_delete_non_existant_question(self):
      '''Tests deletinging non-existant question returns 422'''

      num_questions_before = Question.query.all()

      res = self.client().delete(f'/questions/1000')
      data = json.loads(res.data)

      num_questions_after = Question.query.all()

      self.assertEqual(res.status_code, 422)
      self.assertEqual(data['success'], False)
      self.assertTrue(len(num_questions_before) == len(num_questions_after))

    def test_search_questions(self):
      '''Tests a successful search'''

      res = self.client().post('/questions', json={'searchTerm': 'hematology'})
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)

      # check that number of results is 1
      self.assertEqual(len(data['questions']), 1)

    def test_play_quiz(self):
      '''Tests playing quiz successfully '''

      res = self.client().post('/quizzes', json={'previous_questions': [17,18], 'quiz_category': {'type': 'Art', 'id': '2'}})

      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)

      # test that a question is returned and is in correct category
      self.assertTrue(data['question'])
      self.assertEqual(data['question']['category'], 2)

      # test that question returned has is not in previous_questions
      self.assertNotEqual(data['question']['id'], 17)
      self.assertNotEqual(data['question']['id'], 18)

    def test_play_quiz_fails(self):
      '''Tests playing quiz fails '''

      res = self.client().post('/quizzes', json={})
      data = json.loads(res.data)

      # check response status code and message
      self.assertEqual(res.status_code, 400)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()