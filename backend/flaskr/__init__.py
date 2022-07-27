import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import true

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def retrieve_categoreis():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {}

        if request.args:
            abort(400)

        for category in categories:
            formatted_categories[category.id] = category.type

        if len(formatted_categories) == 0:
            abort(404)

        return jsonify({
          'categories': formatted_categories
        }), 200

    @app.route('/questions')
    def retrieve_questions():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        formatted_questions = [q.format() for q in questions]
        paginated_questions = formatted_questions[start:end]

        if len(paginated_questions) == 0:
            abort(404)

        formatted_categories = {}

        for category in categories:
            formatted_categories[category.id] = category.type

        # Get the last question and return it's category as currentCategory
        last_question = paginated_questions[-1]
        last_category_id = last_question['category']
        current_category = formatted_categories[last_category_id]

        return jsonify({'questions': paginated_questions,
                        'totalQuestions': len(questions),
                        'categories': formatted_categories,
                        'currentCategory': current_category}), 200

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({"id": question_id})
        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_questions():
        body = request.get_json()

        try:
            new_question = Question(question=body.get('question', None),
                                    answer=body.get('answer', None),
                                    category=body.get('category', None),
                                    difficulty=body.get('difficulty', None))

            new_question.insert()

            return jsonify({'success': True}), 200
        except Exception:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()

        if request.args:
            abort(400)

        search_term = body['searchTerm']
        questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search_term))).all()

        if len(questions) == 0:
            return jsonify({'questions': [],
                            'totalQuestions': 0,
                            'currentCategory': None}), 200

        formatted_questions = [q.format() for q in questions]

        # Get the last question and return it's category as currentCategory
        last_question = formatted_questions[-1]
        last_category_id = last_question['category']
        current_category = Category.query.filter_by(
                            id=last_category_id).one_or_none()
        current_category_type = current_category.type

        return jsonify({'questions': formatted_questions,
                        'totalQuestions': len(formatted_questions),
                        'currentCategory': current_category_type}), 200

    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id):
        questions = Question.query.filter_by(category=category_id).all()
        fornattted_questions = [q.format() for q in questions]
        current_category = Category.query.filter_by(
                          id=category_id).one_or_none()

        if current_category is None:
            abort(404)

        return jsonify({'questions': fornattted_questions,
                        'totalQuestions': len(fornattted_questions),
                        'currentCategory': current_category.type}), 200

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        body = request.get_json()
        try:
            category_id = body['quiz_category']['id']
        except KeyError:
            category_id = None

        past_questions_ids = body['previous_questions']

        # if category id is not zero or None, fetch questions using category id
        if category_id:
            questions = Question.query.filter_by(category=category_id).all()
            # Abort 404 if no question was returned, invalid category id
            if len(questions) == 0:
                abort(404)
        else:
            questions = Question.query.all()

        # If there are no more questions return None
        if len(questions) == len(past_questions_ids):
            return jsonify({'question': None}), 200

        while True:
            question = random.choice(questions)

            if question.id not in past_questions_ids:
                formatted_question = question.format()
                break

        return jsonify({
          'question': formatted_question
          }), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
              "success": False,
              "error": 422, "message": "unprocessable"}), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 405,
          "message": "method not allowed"}), 405

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 500,
          "message": "internal server error"}), 500

    return app
