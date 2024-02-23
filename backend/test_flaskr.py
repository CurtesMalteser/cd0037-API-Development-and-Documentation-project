import unittest
from flaskr import create_app

import os
username = os.environ.get('USER', os.environ.get('USERNAME'))
database_name = "trivia_test"
database_path = "postgresql://{}:{}@{}/{}".format(username, username,'localhost:5432', database_name)


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
    def test_get_books_success(self):
        res = self.client().get('/categories')

        self.assertEqual(200, res.status_code)
        json = res.get_json()

        self.assert_categories_equal(json)

    def test_get_questions_success(self):
        res = self.client().get('/questions?page=1')

        self.assertEqual(200, res.status_code)
        json = res.get_json()

        self.assertTrue(json.get('success'))
        self.assert_categories_equal(json)
        self.assertEqual(10, len(json.get('questions')))
        self.assertEqual(19, json.get('total_questions'))

    def test_get_questions_404_due_to_page_100_not_found(self):
        res = self.client().get('/questions?page=100')

        self.assertEqual(404, res.status_code)
        json = res.get_json()
        self.assertFalse(json.get('success'))


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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()