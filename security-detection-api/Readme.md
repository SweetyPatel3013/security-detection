# Cloud deployment

## Local Env
1. Go to the repo directory
2. Go to the folder security-detection-api  "cd security-detection-api"
3. Run next commands if you haven't install the package yet
    pip install -r requirements.txt
    pip install dlib
4. Run the next command to deploy the app
    python app.py
5. Open the url http://127.0.0.1:8080

## Heroku
1. heroku container:login
2. heroku create --app security-detection-api 
3. heroku container:push web --app security-detection-api
4. heroku container:release web --app security-detection-api
5. heroku open --app security-detection-api

URL: https://security-detection-api.herokuapp.com/

## Google
1. gcloud app deploy app.yml
2. gcloud app logs tail -s default
3. gcloud app browse -s default

### Stop service (Google)
1. gcloud app versions stop --service default {version_id}

## Azure
Azure: https://security-detection-api.azurewebsites.net

## Run app using docker image built and saved in Docker hub
**Run**
- docker run -it --cpus="2" -p 5000:8080 mcadac/security-detection-api:1.0.1

### Commands to build and push image in the docker hub
**Build docker image**
- docker build -t mcadac/security-detection-api:1.0.1 .

**Push docker image**
- docker push mcadac/security-detection-api:1.0.1
