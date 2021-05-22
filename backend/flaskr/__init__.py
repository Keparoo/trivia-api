#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

#----------------------------------------------------------------------------#
# App Config
#----------------------------------------------------------------------------#

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  # CORS setup: allow all origins
  CORS(app, resources={r"/*": {"origins": "*"}})

  # setup CORS Headers and allowed methods
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
    return response

#----------------------------------------------------------------------------#
# Helper Functions
#----------------------------------------------------------------------------#

  QUESTIONS_PER_PAGE = 10

  def paginate_questions(request, selection):
    ''' paginate questions in selection '''

    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

#----------------------------------------------------------------------------#
# Define API Endpoints
#----------------------------------------------------------------------------#
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():
    '''
    This endpoint handles GET requests to /categories
    It returns
    a success flag,
    an object of categories in which the keys are the ids and the value is the corresponding string of the category
    '''

    categories = Category.query.order_by(Category.id).all()

    # check if categories returned is empty
    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in categories}
    })
  
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    '''
    This endpoint handles GET requests to /questions
    It returns a object containing:
    a success flag
    a paginated list of all questions (pages of 10),
    the number of total questions,
    an dictionary of all categories,
    the current category
    '''
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    # check if list of questions is empty
    if len(current_questions) == 0:
      abort(404)

    # check if list of categories is empty
    categories = Category.query.order_by(Category.id).all()
    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions, 
      'total_questions': len(selection),
      'categories': {category.id: category.type for category in categories},
      'current_category': None
    })

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    ''' 
    This endpoint handles DELETE requests to /questions/<question_id>
    The question matching id will be deleted
    It returns a success flag and the id of the deleted question
    '''
      
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      # return 404 if question id doesn't exist
      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id
      })

    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():
    '''
    Handles POST requests for searching for and creating new questions
    If a search term is sent, it will return:
    a success flag,
    a paginated list of questions matching the search term
    the total number of matching questions
    the current category (None)

    If no search term is sent it will create a new question from posted data:
    question, answer, difficulty, category
    It will return a success flag
    the id of the new question
    '''
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)
    search_term = body.get('searchTerm', None)

    try:
      # Check if searching or creating new question
      if search_term:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike(f'%{search_term}%'))

        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(selection.all()),
          'currentCategory': None
        })
      else:
      # if no search term, create an new question

        # make sure all fields are populated
        if ((new_question is None) or (new_answer is None) or (new_difficulty is None) or (new_category is None)):
          abort(422)
  
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
        question.insert()

        return jsonify({
          'success': True,
          'question_id': question.id
        })

    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
  def retrieve_questions_by_category(cat_id):
    '''
    Handles GET requests for searching for questions based on catgory
    It will return a success flag,
    a paginated list of questions matching the id of the category,
    the total number of matching questions,
    the current category
    '''
    
    try:
      category = Category.query.filter_by(id=cat_id).one_or_none().format()['type']
    
    # return 404 if no category exists
    except:
      abort(404)

    try:
      questions = Question.query.filter(Question.category == cat_id).all()
      current_questions = paginate_questions(request, questions)

      return jsonify({
        'success': True,
        'questions': current_questions, 
        'total_questions': len(questions),
        'current_category': category
      })

    except:
      abort(404)

  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    '''
    Handles POST request for playing the quiz game
    Expects a list of questions already asked,
    A Category (If category is all, id=-0)
    Returns a random unasked question matching the category
    '''

    body = request.get_json()

    # parse body data
    previous_questions = body.get('previous_questions', None)
    category = body.get('quiz_category', None)

    # Check that all fields have data
    if ((category is None) or (previous_questions is None)):
      abort(400)

    # load questions from all categories
    if (category['id'] == 0):
      questions = Question.query.all()

    # load questions for specific category
    else:
      questions = Question.query.filter_by(category=category['id']).all()

    random.shuffle(questions)

    # find question that hasn't been asked
    found = False
    for question in questions:
      if not question.id in previous_questions:
        found = True
        break
    
    # All questions have been asked or less than 5 questions in category
    if not found:
      return jsonify({
      'success': True,
      'question': None
    })
    
    # return new unasked question
    return jsonify({
      'success': True,
      'question': question.format()
    })

#----------------------------------------------------------------------------#
# Define Error Handlers
#----------------------------------------------------------------------------#
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400

  return app

    