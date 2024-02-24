import random
from unicodedata import category
from flask import (
    Flask,
    request,
    abort,
    jsonify,
    )
from flask_cors import CORS
from models import (
    Question,
    QuestionDecoder,
    db,
    setup_db,
    )
import json

from request_utils import *

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = str(test_config.get('SQLALCHEMY_DATABASE_URI'))
        setup_db(app, database_path = database_path)

    """
    @Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    """
    Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = get_categories_or_none()
        if categories is None:
                abort(400)
        else:
            return jsonify({
                'categories': categories,
                'success': True
                })
            

    """
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        query=Question.query.order_by(Question.id).all()
        questions = paginate_questions_or_none(request, query)
    
        if questions is None:
            abort(404)
        else:
            return questions
            

    """
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question_by_id(id: int):
        error = None
        try:
            question = Question.query.filter(Question.id == id).one_or_none()
            if question is None:
                error = 404
            else:
                question.delete()
        except:
            error = 500
            db.session.rollback()
        finally:
            db.session.close()
            if isinstance(error, int):
                abort(error)
            else:
                return jsonify({"success": True})

    """
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def search_questions():
        if (request.is_json):
            body = request.get_json()
            search = body.get('searchTerm')

            if isinstance(search, str):

                query = Question.query.filter(Question.question.ilike('%{}%'.format(search))).order_by(Question.id).all()
                questions = paginate_questions_or_none(request, query)
                if questions is None:
                    abort(404)
                else:
                    return questions
            else:
                try:
                    question : Question = json.loads(json.dumps(body), cls=QuestionDecoder)
                    question.insert()
                    return jsonify({"success": True})
                except:
                    db.session.rollback()
                    abort(422)
                finally:
                    db.session.close()
        else:
            abort(400)

    """
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id: int):
        query = Question.query.filter(Question.category == id).order_by(Question.id).all()
        questions = paginate_questions_or_none(request, category_id=id, query=query)
    
        if questions is None:
            abort(404)
        else:
            return questions

    """
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def random_question():
        if (request.is_json):
            body = request.get_json()
            previous_questions = body['previous_questions']

            if previous_questions is None:
                abort(422)

            category_id = body['quiz_category']['id']
            if category_id is None:
                abort(422)

            questions = Question.query.order_by(Question.id).all()

            if int(category_id) > 0:
                questions = [question for question in questions if str(question.category) == category_id]
                questions = [question for question in questions if question.id not in previous_questions]

            question = None

            if len(questions) > 0:
                question = random.choice(questions).format()


            return jsonify({
                "previousQuestions": body['previous_questions'],
                "question": question,
                "success": True
                })
        else:
            abort(400)
    """
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def not_there(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad request",
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found",
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable Content",
            }), 422

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Internal Server Error",
            }), 500

    return app

