
heroku container:login
heroku create --app security-detection-api 
heroku container:push web --app security-detection-api
heroku container:release web --app security-detection-api
heroku open --app security-detection-api
