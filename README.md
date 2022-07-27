# Full Stack API Final Project

## Full Stack Trivia
This project is part of the Udacity Full Stack Nanodegree program. It's a fun app where you get to answer questions and you are graded after each round. Each round consists of five questions, and if there are less than five questions in the chosen category the game exits and grades you. You can either pick a category to answer questions on or just choose to answer general questions. The front end was built  by the udacity team and i built the database backed API to play the game. It's a fun way to test out my newly acquired skills on API developement.

**Project status: Complete**
You should feel free to expand on the project in any way you can.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 
The backend folder contains a .env file where environment variables should be stored. The environment variable should be used to store database information, optionally the FLASK_APP and FLASK_ENV variables should be stored there also.

To run the application run the following commands if FLASK_APP and FLASK_ENV are not set in the .env file:
 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
else, you should run the command:
```
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

#### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 


## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: Method Not Allowed
- 500: Internal Server Error

### Endpoints 

#### GET /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs. 
```
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

#### GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
```
{
    'questions': [
        {
          "answer": "Apollo 13",
          "category": 5,
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
    ],
    'totalQuestions': 18,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'Art'
}
```

#### GET '/categories/${id}/questions'
- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string 
```
{
    'questions': [
        {
          "answer": "The Liver",
          "category": 1,
          "difficulty": 4,
          "id": 20,
          "question": "What is the heaviest organ in the human body?"
        },
        {
          "answer": "Alexander Fleming",
          "category": 1,
          "difficulty": 3,
          "id": 21,
          "question": "Who discovered penicillin?"
        },
    ],
    'totalQuestions': 4,
    'currentCategory': 'Science'
}
```

#### DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: the id of the object deleted
```
{
    'id': 20
}
```


#### POST '/quizzes'
- Sends a post request in order to get the next question 
- Request Body: 
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
- Returns: a single new question object 
```
{
    'question': {
        'id': 1,
        'question': 'What's the fastest way to level up your tech skills?',
        'answer': 'Take a course on Udacity', 
        'difficulty': 5,
        'category': 4
    }
}
```

#### POST '/questions'
- Sends a post request in order to add a new question
- Request Body: 
```
{
    'question':  'Who is the founder of udacity',
    'answer':  'Sebastin Thrun',
    'difficulty': 1,
    'category': 3,
}
```
- Returns: A success message
```
{
    'success': True
}
```
#### POST '/questions/search'
- Sends a post request in order to search for a specific question by search term 
- Request Body: 
```
{
    'searchTerm': 'this is my search term'
}
```
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
```
{
    'questions': [
        {
            'id': 1,
            'question': 'what is the largest lake in Africa',
            'answer': 'Lake Victoria', 
            'difficulty': 2,
            'category': 3
        },
    ],
    'totalQuestions': 16,
    'currentCategory': 'Geography'
}
```

## Authors
Iyamu Hope Nosa, Udacity team

## Acknowledgements 
The awesome team at Udacity, and my fellow ALX-FSND students! 


