
from operator import is_not
from flask import abort, jsonify
from models import Question, Category

QUESTIONS_PER_PAGE = 10

def is_valid_category_id(category_id, categories):
    return category_id and category_id in map(lambda category: category.id, categories)

def get_categories_or_none(category_id = None):
        categories = Category.query.all()
        
        if is_not(None, categories):
            is_valid_category =  is_valid_category_id(category_id, categories) if category_id else True 

            if is_valid_category:
                return { str(category.id): category.type for category in categories }
            else:
                return None
        else:
            return None

def paginate_questions_or_none(request, category_id = None):
    page = request.args.get('page', 1, type=int)
    
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    categories = get_categories_or_none(category_id)

    if categories is None:
        abort(400)

    questions = []

    try:
        if category_id is None:
            questions = Question.query.order_by(Question.id).all()
        else:
            questions = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
    except Exception as e:
        abort(500)

    if questions is None:
        abort(400)

    total_questions = len(questions)

    questions = map(lambda  question: question.format(), questions)
    questions = list(questions)[start:end]


    if len(questions) > 0:
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': total_questions,
            'categories': categories,
            'current_category': category_id if category_id else 0
            })
    else:
        return None