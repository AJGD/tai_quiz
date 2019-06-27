This project is a Django application for creating and solving knowledge-testing quizzes, with the added caveat that the questions 
for said quizzes are generated based on Wikipedia assets. 

## Building the project locally

### With Docker

First, delete or comment out the last line in `Dockerfile` (it's indicated by a comment). Then from the root directory use 
`docker-compose up`. If everything goes right the application should be available on `127.0.0.1:8000`.

### Without Docker

You'll need `pip` and `python` (since this is a Django project). In the `tai_quiz/quiz` directory execute:

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

As before, the application should be available on `127.0.0.1:8000`.
