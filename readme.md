# Ask Clone

Ask Clone is a Django application that provides functionalities related to user registration, user profiles, questions, and question posts.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/AskCloneApi

```
2. Create a virtual environment:
```bash
python3 -m venv env
source env/bin/activate
```
3. Install the dependencies:
```bash
pip install -r requirements.txt

```
4. Apply database migrations:
```bash
python manage.py migrate

```
5. Run the development server:
```bash
python manage.py runserver
```

6. Access the application at [http://localhost:8000/](http://localhost:8000/)

## Features

- User Registration: Allows users to register and create an account.
- User Profiles: Provides the ability to create and manage user profiles with description, Facebook, and Twitter links.
- Questions: Enables users to ask questions and view a list of all questions.
- Question Posts: Allows users to post answers (question posts) to existing questions.
- JWT Token Authentication: Uses JWT authentication for secure API endpoints.
- API Endpoints: Provides various API endpoints for user registration, user profiles, questions, and question posts.

## API Endpoints

- `/api/register`: POST request to register a new user.
- `/api/profile`: POST request to create or update a user profile.
- `/api/token`: POST request to obtain a JWT token.
- `/api/token/refresh`: POST request to refresh a JWT token.
- `/api/create`: POST request to create a new question.
- `/api/questions`: GET request to list all questions.
- `/api/createpost`: POST request to create a new question post (answer).
- `/api/listquestionpost`: GET request to list all question posts.
- `/api/deletequestionpost/<int:pk>`: DELETE request to delete a question post by its ID.
- `/api/retrievequestionpost/<int:pk>`: GET request to retrieve a question post by its ID.
- `/api/updatequestionpost/<int:pk>`: PUT request to update a question post by its ID.
- `/api/question/<int:pk>`: GET request to retrieve a question and its associated question posts by its ID.
<<<<<<< HEAD
=======

>>>>>>> 4891f1a2752f22dcc4aca93ef0ce2761f68b34a7
