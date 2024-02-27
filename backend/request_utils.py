
from operator import is_not
from flask import abort, jsonify
from models import Category

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

def paginate_questions_or_none(request, query, category_id = None):
    page = request.args.get('page', 1, type=int)

    categories = get_categories_or_none(category_id)

    if categories is None:
        abort(400)

    questions = []

    total_questions = 0
    
    try:
        questions = query.paginate(page, QUESTIONS_PER_PAGE, False).items
        total_questions = query.count()
    except Exception as e:
        print('🧨 error: {}'.format(e))
        abort(500)

    if questions is None:
        abort(400)

    questions = map(lambda  question: question.format(), questions)
    questions = list(questions)


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