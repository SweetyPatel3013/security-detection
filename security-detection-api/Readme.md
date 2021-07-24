# Cloud deployment

## Heroku
heroku container:login
heroku create --app security-detection-api 
heroku container:push web --app security-detection-api
heroku container:release web --app security-detection-api
heroku open --app security-detection-api

## Google
gcloud app deploy app.yml
gcloud app logs tail -s default
gcloud app browse -s default
# Stop service
 gcloud app versions stop --service default {version_id}
