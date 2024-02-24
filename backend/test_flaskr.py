import unittest
from flaskr import create_app

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

    def test_search_questions_400_missing_content_type_application_json_header(self):
        res = self.client().post('/questions', data='{"searchTerm": "tom"}')
        self.assert_400_true(res)

    def test_search_questions_404_questions_not_found_for_given_search_term(self):
        res = self.client().post('/questions', data='{"searchTerm": "noSearchTermMatches"}', content_type='application/json')
        self.assert_404_true(res)

    def test_search_questions_422_questions_not_found_for_given_search_term(self):
        res = self.client().post('/questions', data='{"malformed": "json"}', content_type='application/json')

        self.assertEqual(422, res.status_code)
        json = res.get_json()
        self.assertFalse(json.get('success'))
        self.assertEqual('Unprocessable Content', json.get('message'))

    def test_add_question_success(self):
        data = '{"question": "Test question?", "answer": "Test", "difficulty": "3", "category": "2"}'
        res = self.client().post('/questions', data=data, content_type='application/json')

        self.assertEqual(200, res.status_code)
        self.assertTrue(res.get_json().get('success'))

    def test_delet_question_success(self):
        res = self.client().delete('/questions/5')

        self.assertEqual(200, res.status_code)
        self.assertTrue(res.get_json().get('success'))

    def test_delet_question_404_not_found_for_id(self):
        res = self.client().delete('/questions/100')
        self.assert_404_true(res)

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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()