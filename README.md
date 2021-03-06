# Full Stack Trivia API Project

This project is a trivia game where users can test their knowledge in different trivia categories: *Science, Art, Geography, History, Entertainment, and Sports*. The goal of this project was to complete a RESTful API, test suite and documentation that implements the following functionality:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.
---
## Getting Started

### Installing Dependencies

Development for this project requires **Python 3.6** or later, **Nodejs**, **pip** and the Node Package Manager (**NPM**) to be already installed.

#### Frontend Dependencies

This project uses NPM to manage software dependencies. The required dependencies are found in the `/frontend/package.json` file located of this repository. After cloning the repository, open your terminal navigate to the `/frontend` folder and run:

    npm install

#### Backend Dependencies

Setup and run a Python 3.6 or later virtual environment, navigate to the `/backend` directory and run:

    pip install -r requirements.txt

### Running Your Frontend in Developer Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. The start script is located in `/frontend/package.json` file if you need to adapt it.

    npm start

The frontend is hosted at `http://localhost:3000`  
Open `http://localhost:3000` to view the web app in the browser. The page will automatically reload if you make edits.

### Running the Backend Server

From within the `/backend` directory activate the virtual environment and run the backend server.

To run the server, execute:

    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run --reload

The `--reload` flag will detect file changes and restart the backend server automatically.

### Testing

Tests are contained in the `/backend/test_flaskr.py` file.  
To run the tests, execute:  
(The first time you run tests, omit the dropdb command)

    dropdb trivia_test
    createdb trivia_test
    psql trivia_test < trivia.psql
    python test_flaskr.py
---
## API Reference

### Getting Started
* Base URL: This application is hosted locally. The backend is hosted at `http://127.0.0.1:5000/` 
* Authentication: This application currently does not require authentication or API keys

### Error Handling

Errors are returned as a JSON object.

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API currently returns three classes of errors:

* 400 ??? bad request 
* 404 ??? resource not found  
* 422 ??? unprocessable
---
### API Endpoints

#### GET /categories

* Returns a list of categories
* Returns a success flag
* Test: `curl http://127.0.0.1:5000/categories`  
Response body:

      {
          "categories": {
              "1": "Science", 
              "2": "Art", 
              "3": "Geography", 
              "4": "History", 
              "5": "Entertainment", 
              "6": "Sports"
          }, 
          "success": true
      }

#### GET /questions
#### GET /questions?page=${integer}

* Returns a list of questions
* Results are paginated 10 to a page
* Returns a list of categories
* Returns the total number of questions
* Optional URL request argument: `?page=`
* Returns a success flag

Test: `curl http://127.0.0.1:5000/questions`  
Response body:
    
    {
      "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
       "6": "Sports"
      },
      "questions": [
        {
          "answer": "Apollo 13", 
          "category": 5, 
          "difficulty": 4, 
          "id": 2, 
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }, 
        {
          "answer": "Tom Cruise", 
          "category": 5, 
          "difficulty": 4, 
          "id": 4, 
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }, 
        {
          "answer": "Maya Angelou", 
          "category": 4, 
          "difficulty": 2, 
          "id": 5, 
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, 
        {
          "answer": "Edward Scissorhands", 
          "category": 5, 
          "difficulty": 3, 
          "id": 6, 
          "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }, 
        {
          "answer": "Muhammad Ali", 
          "category": 4, 
          "difficulty": 1, 
          "id": 9, 
          "question": "What boxer's original name is Cassius Clay?"
        }, 
        {
          "answer": "Brazil", 
          "category": 6, 
          "difficulty": 3, 
          "id": 10, 
          "question": "Which is the only team to play in every soccer World Cup tournament?"
        }, 
        {
          "answer": "Uruguay", 
          "category": 6, 
          "difficulty": 4, 
          "id": 11, 
          "question": "Which country won the first ever soccer World Cup in 1930?"
        }, 
        {
          "answer": "George Washington Carver", 
          "category": 4, 
          "difficulty": 2, 
          "id": 12, 
          "question": "Who invented Peanut Butter?"
        }, 
        {
          "answer": "Lake Victoria", 
          "category": 3, 
          "difficulty": 2, 
          "id": 13, 
          "question": "What is the largest lake in Africa?"
        }, 
        {
          "answer": "The Palace of Versailles", 
          "category": 3, 
          "difficulty": 3, 
          "id": 14, 
          "question": "In which royal palace would you find the Hall of Mirrors?"
        }
      ], 
      "success": true, 
      "total_questions": 20
    }

#### DELETE /questions/\<int:id\>

* Deletes a question from the database by id as a URL parameter
* Returns the id of the deleted question if successful
* Returns a success flag

Test: `curl http://127.0.0.1:5000/questions/3 -X DELETE`  
Response body:

      {
          "deleted": 3, 
          "success": true
      }
      
#### POST /questions

This endpoint handles two functions:
1. If a search term is included in the request it will search questions returning all matches
2. If no search term is included it will create a new question and insert it into the database  


If a search term is included in the request, the endpoint:

* Searches database for matching questions 
* Returns a paginated JSON object with all matching questions (case insensitive)
* Returns the total number of matching questions
* Returns a success flag

Test: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "name"}'`  
Response body:

    {
      "questions": [
        {
          "answer": "Muhammad Ali", 
          "category": 4, 
          "difficulty": 1, 
          "id": 9, 
          "question": "What boxer's original name is Cassius Clay?"
        }, 
        {
          "answer": "Brazil", 
          "category": 6, 
          "difficulty": 3, 
          "id": 10, 
          "question": "Which is the only team to play in every soccer World Cup tournament?"
        }
      ], 
      "success": true, 
      "total_questions": 2
    }

If there is no search term in the request, the endpoint:

* Creates a new question using the JSON parameters and inserts it into database
* Returns the questions id
* Returns a success flag

Test: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Which particle binds quarks in a nucleus", "answer": "gluon", "difficulty": 4, "category": "1" }'`  
Response body:

    {
      "question_id": 32, 
      "success": true
    }
  
#### GET /categories/\<int:id>\/questions

* Searches for questions matching the category id using URL parameters
* Returns a paginated JSON object of matching questions
* Returns the current category
* Returns the total number or matching questions
* Returns a success flag

Test: `curl http://127.0.0.1:5000/categories/1/questions`  
Response body:

      {
          "current_category": "Science", 
          "questions": [
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
              {
                  "answer": "Blood", 
                  "category": 1, 
                  "difficulty": 4, 
                  "id": 22, 
                  "question": "Hematology is a branch of medicine involving the study of what?"
              }
          ], 
          "success": true, 
          "total_questions": 3
      }

#### POST /quizzes

* Facilitates playing a quiz game
* Accepts the following JSON request paramaters:
  * category
  * list of id numbers of questions already asked
* Returns a JSON object with a random question not yet asked
* Returns a success flag

Test: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [17, 18], "quiz_category": {"type": "Art", "id": "2"}}'`  
Response body:

    {
      "question": {
        "answer": "Escher", 
        "category": 2, 
        "difficulty": 1, 
        "id": 16, 
        "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
      }, 
      "success": true
    }

### Authors
Kep Kaeppeler is the author of the backend API, test suite, and documentation including the `__init__.py`, `test_flaskr.py`, and this `README` file.  
All other project files, including the models and frontend, were created by the Udacity team. This was meant as a project template for the Full Stack Web Developer Nanodegree.
  