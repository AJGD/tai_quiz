FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /tai_quiz

WORKDIR /tai_quiz

ADD . /tai_quiz

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# for local deployment delete or comment out the line below and use "docker-compose up" instead.
CMD  bash -c "cd ./quiz && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT"