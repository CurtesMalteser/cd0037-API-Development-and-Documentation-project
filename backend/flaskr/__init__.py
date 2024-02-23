from operator import is_not
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def get_categories_or_none():
        categories = Category.query.all()

        if is_not(None, categories):
            return { str(category.id): category.type for category in categories }
        else:
            return None

def paginate_questions_or_none(request):
    page = request.args.get('page', 1, type=int)
    
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = []
    
    try:
        questions = Question.query.order_by(Question.id).all()
    except:
        abort(500)

    if questions is None:
        abort(400)

    total_questions = len(questions)

    questions = map(lambda  question: question.format(), questions)
    questions = list(questions)[start:end]

    categories = get_categories_or_none()

    if categories is None:
        abort(400)

    if len(questions) > 0:
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': total_questions,
            'categories': categories#,
            # 'currentCategory': "Science",  todo: fill with selected
            # -> extract the dic and add if it's a request with a selected category
            # -> pass query as args or bassed on existence of category arg, run proper query
            # -> either all or select by category
            })
    else:
        return None

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
            return jsonify({'categories': categories})
            

    """
    @TODO:
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
        questions = paginate_questions_or_none(request)
    
        if questions is None:
            abort(404)
        else:
            return questions
            

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
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
 
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Internal Server Error",
            }), 500

    return app

