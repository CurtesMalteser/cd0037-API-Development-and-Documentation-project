import unittest
from flaskr import create_app
import json

import os
username = os.environ.get('USER', os.environ.get('USERNAME'))
database_name = "trivia_test"
database_path = "postgresql://{}:{}@{}/{}".format(username, username,'localhost:5432', database_name)


from models import db, Question

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = database_name
        self.database_path = database_path
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_success(self):
        res = self.client().get('/categories')

        self.assertEqual(200, res.status_code)
        json = res.get_json()

        self.assert_categories_equal(json)
        self.assertTrue(json.get('success'))

    def test_get_questions_success(self):
        res = self.client().get('/questions?page=1')


        self.assertEqual(200, res.status_code)
        json = res.get_json()

        self.assertTrue(json.get('success'))
        self.assert_categories_equal(json)
        self.assertEqual(10, len(json.get('questions')))
        self.assertEqual(0, json.get('current_category'))

    def test_get_questions_404_due_to_page_100_not_found(self):
        res = self.client().get('/questions?page=100')
        self.assert_404_true(res)

    def test_get_questions_by_category_success(self):
        expected_category_sport=6
        res = self.client().get('/categories/{}/questions'.format(expected_category_sport))

        self.assertEqual(200, res.status_code)
        json = res.get_json()

        self.assertTrue(json.get('success'))
        self.assert_categories_equal(json)
        self.assertEqual(2, len(json.get('questions')))
        self.assertEqual(2, json.get('total_questions'))
        self.assertEqual(expected_category_sport, json.get('current_category'))

    def test_get_questions_by_category_400_due_to_non_existing_category(self):
        res = self.client().get('/categories/{}/questions'.format(20))
        self.assertEqual(400, res.status_code)

        json = res.get_json()
        self.assertFalse(json.get('success'))
        self.assertEqual('Bad request', json.get('message'))


    def test_get_questions_by_category_404_no_questions_for_category(self):
        category_id = 1
        db.session.query(Question).filter(Question.category == category_id).delete()

        res = self.client().get('/categories/{}/questions'.format(1))

        db.session.commit()
        db.session.close()

        self.assert_404_true(res)

    def test_search_questions_success(self):
        res = self.client().post('/questions', data='{"searchTerm": "tom"}', content_type='application/json')

        self.assertEqual(200, res.status_code)
        json = res.get_json()

        self.assertTrue(json.get('success'))
        self.assert_categories_equal(json)
        self.assertEqual(1, len(json.get('questions')))
        self.assertEqual(1, json.get('total_questions'))
        self.assertEqual(0, json.get('current_category'))

    def test_search_questions_400_missing_content_type_application_json(self):
        res = self.client().post('/questions', data='{"searchTerm": "tom"}')
        self.assert_400_true(res)

    def test_search_questions_404_questions_not_found_for_given_search_term(self):
        res = self.client().post('/questions', data='{"searchTerm": "noSearchTermMatches"}', content_type='application/json')
        self.assert_404_true(res)

    def test_search_questions_422_questions_not_found_for_given_search_term(self):
        res = self.client().post('/questions', data='{"malformed": "json"}', content_type='application/json')
        self.assert_422_true(res)

    def test_add_question_success(self):
        data = '{"question": "Test question?", "answer": "Test", "difficulty": 3, "category": 2}'
        res = self.client().post('/questions', data=data, content_type='application/json')

        self.assertEqual(200, res.status_code)
        self.assertTrue(res.get_json().get('success'))

    def test_delete_question_success(self):
        res = self.client().delete('/questions/5')

        self.assertEqual(200, res.status_code)
        self.assertTrue(res.get_json().get('success'))

    def test_delete_question_404_not_found_for_id(self):
        res = self.client().delete('/questions/100')
        self.assert_404_true(res)

    def test_post_quizzes_success(self):
        previous_questions = list([5, 9, 2])
        category_id = 1
        data = json.dumps({"previous_questions": previous_questions, "quiz_category": {"id": category_id}}) 
        res = self.client().post('/quizzes', data=data, content_type='application/json')

        self.assertEqual(200, res.status_code)
        json_response = res.get_json()

        self.assertTrue(json_response['success'])
        self.assertEqual(previous_questions, json_response['previousQuestions'])
        self.assertIsNotNone(json_response['question'])
        self.assertIsNotNone(json_response['question']['id'])
        self.assertIsNotNone(json_response['question']['answer'])
        self.assertIsNotNone(json_response['question']['difficulty'])
        self.assertEqual(category_id, json_response['question']['category'])
        self.assertIsNotNone(json_response['question']['question'])

    def test_post_quizzes_sport_category_returns_no_question_after_answer_all_questions(self):
        previous_questions = list([10, 11])
        category_id = 6
        data = json.dumps({"previous_questions": previous_questions, "quiz_category": {"id": category_id}}) 
        res = self.client().post('/quizzes', data=data, content_type='application/json')

        self.assertEqual(200, res.status_code)
        json_response = res.get_json()

        self.assertTrue(json_response['success'])
        self.assertEqual(previous_questions, json_response['previousQuestions'])
        self.assertIsNone(json_response['question'])

    def test_post_quizzes__400_missing_content_type_application_json(self):
        res = self.client().post('/quizzes', data='{"previous_questions": [1, 2, 3], "quiz_category": {"id": 1}}')
        self.assert_400_true(res)

    def test_post_quizzes_422_malformed_json(self):
        res = self.client().post('/quizzes', data='{"malformed": "json"}', content_type='application/json')
        self.assert_422_true(res)

    def test_post_quizzes__422_missing_category_id(self):
        res = self.client().post('/quizzes', data='{"previous_questions": [1, 2, 3]}', content_type='application/json')
        self.assert_422_true(res)

    def test_post_quizzes__422_missing_previous_questions(self):
        res = self.client().post('/quizzes', data='{"quiz_category": {"id": 1}}', content_type='application/json')
        self.assert_422_true(res)

    # Helper function to assert all categories are in the json response
    def assert_categories_equal(self, json):
        actual_categories = json.get('categories')

        expected_categories = {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
            }

        self.assertEqual(expected_categories, actual_categories)

    # Helper function to assert 404 and json response is correct
    def assert_404_true(self, res):
        self.assertEqual(404, res.status_code)
        json = res.get_json()
        self.assertFalse(json.get('success'))
        self.assertEqual('Not found', json.get('message'))

        # Helper function to assert 400 and json response is correct
    def assert_400_true(self, res):
        self.assertEqual(400, res.status_code)
        json = res.get_json()
        self.assertFalse(json.get('success'))
        self.assertEqual('Bad request', json.get('message'))

    # Helper function to assert 422 and json response is correct
    def assert_422_true(self, res):
        self.assertEqual(422, res.status_code)
        json = res.get_json()
        self.assertFalse(json.get('success'))
        self.assertEqual('Unprocessable Content', json.get('message'))
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()