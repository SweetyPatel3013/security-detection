FROM docker.io/mcadac/tensorflow:base-security-docker-image

COPY . /opt/app
WORKDIR /opt/app

# Expose is NOT supported by Heroku
EXPOSE 8080

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
#CMD gunicorn --bind 0.0.0.0:$PORT wsgi

# Local and Google cloud
CMD gunicorn --bind 0.0.0.0:8080 wsgi