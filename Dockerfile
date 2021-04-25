FROM python:3.9

WORKDIR /app
RUN pip install pipenv

COPY Pipfile* /app
RUN pipenv install --system --deploy

COPY . /app

USER 1000

ENV FLASK_APP=video_gallery.wsgi:app
CMD gunicorn --bind 0.0.0.0:5000 video_gallery.wsgi:app

