FROM python:3.7-alpine

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

# Expose is NOT supported by Heroku
EXPOSE 5000

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD gunicorn --bind 0.0.0.0:$PORT wsgi
#CMD gunicorn --bind 0.0.0.0:5000 wsgi