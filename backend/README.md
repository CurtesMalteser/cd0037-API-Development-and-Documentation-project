# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

Optionally you can run

```bash
chmod +x run_test.sh
./run_test.sh
```

## Endpoints documentation

### Get categories
`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with key, `categories`, that contains an object of `id: category_string` key: value pairs and a key, `success` of type boolean `true` if request was successful.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports",
  "success": true
}
```

### Get questions
`GET '/questions'`
`GET '/questions?page=<int>'`

- Fetches a dictionary which contains a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category, a list of questions, number of total questions, current category, and a key success. The list of questions is paginated, where `10` questions are returned per page.
- Request Arguments:
  * optional `page` of type int, where `1` is the default page
- Returns: A [Questions object json](#questions-object-json)

### Delete question
`DELETE '/questions/<int:id>'`

- Deletes a question from the database
- Request Arguments:
  * `id` of type int not null
- Returns: An object with key `success` of type boolean `true` if request was successful
  
```json
{
  "success": true
}
```

### Add question
`POST '/questions'`

- Adds a question to the database

- Request Arguments:
  * key `question` of type string not null
  * key `answer` of type string not null
  * key `category` of type int not null
  * key `difficulty` of type int not null

``` json
{
  "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
  "answer": "Apollo 13",
  "category": 5,
  "difficulty": 4
}
```

- Returns: An object with key `success` of type boolean `true` if request was successful

```json
{
  "success": true
}
```

### Search questions
`POST '/questions'`

- Fetches a list of questions that contain the search term
- Request Arguments:
  * key `searchTerm` of type string not null
- Returns: A [Questions object json](#questions-object-json)
  * key `current_category` is always `0` which represents all categories, since search does not filter by category

## Question object json
- key `answer` of type string not null
- key `category` of type int not null
- key `difficulty` of type int not null
- key `id` of type int not null
- key `question` of type string not null

```json
{
  "answer": "Apollo 13", 
  "category": 5, 
  "difficulty": 4, 
  "id": 2, 
  "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
}
```

## Questions object json

- key `categories`, that contains an object of `id: category_string`
- key `current_category` of type int, where `0` represents all categories
- key `questions` of type list of [Question](#question-object-json) object
- key `success` of type boolean `true` if request was successful
- key `total_questions` of type int, where the total amount of questions is returned

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  },
  "current_category": 0,
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
```

## Expected errors

### 400: Bad request
```json
{
  "error": 400,
  "message": "Bad request",
  "success": false
}
```

### 404: Not found
```json
{
  "error": 404,
  "message": "Not found",
  "success": false
}
```

### 422: Unprocessable
```json
{
  "error": 422,
  "message": "Unprocessable Content",
  "success": false
}
```

### 500: Internal server error
```json
{
  "error": 500,
  "message": "Internal server error",
  "success": false
}
```

## Credits
- [Udacity](https://www.udacity.com/) for providing the starter code and the project idea
- [Flask](http://flask.pocoo.org/) for providing the backend microservices framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for providing the Python SQL toolkit and ORM
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) for providing the extension to handle cross-origin requests from our frontend server

## Authors
- [Udacity](https://github.com/udacity/cd0037-API-Development-and-Documentation-project#:~:text=Contributors,4)
- [António J. Dias Bastião](https://github.com/CurtesMalteser)
```

