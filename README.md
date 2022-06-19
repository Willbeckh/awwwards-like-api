# Project
REST API created with django-rest-framework, 
This api lets users to create projects and add images for them to be rated/reviewed.

## Tech stack
- Django 4.0.4
- Django-rest-framework
- simple jwt(authentication)
- CORS headers (for api cunsumption)

- **Front-end**
  - AngularJs 13
  - Bootstrap
 

## Installation 
1. Clone repo
2. cd into `sturdy-doodle`
3. create virtual environment: (virtualenv, pipenv, conda, e.t.c)
4. install all project dependencies; `pipenv install Pipfile`
5. Run with `python manage.py runserver`

### setup
- create dot-env file `.env`
add the following inside the environment file

```bash
DB_USER = <username >
DB_PASSWORD = <password >
DB_HOST = <host >
DB_PORT = <port >
DB_NAME = <dbname >
SECRET_KEY = <secret_key >
MODE = 'dev'

CLOUDINARY_CLOUD_NAME = <cloud_name >
CLOUDINARY_API_KEY = <api_key >
CLOUDINARY_API_SECRET = <api_secret >
```
# Running
This API can be consumed using a language of your choice.
> Nb: use postman to test.

- for authentication pass in the jwt access token in http headers: 'Authorization Bearer: <acces_token>'
Below are availabe endpoints:
1. [Register](https://looku-awards.herokuapp.com/register): `<link>/register/`
2. [Login](https://looku-awards.herokuapp.com/login) :: `<link>/login/`
3. [Root View](https://looku-awards.herokuapp.com/api) :: `<link>/api/`
4. [Projects view](https://looku-awards.herokuapp.com/api/projects/) :: `<link>/api/projects/`
5. [View single project](https://looku-awards.herokuapp.com/api/projects/1/) :: `<link>/api/projects/`
6. [Rate view](https://looku-awards.herokuapp.com/api/projects/1/rate_project/) :: `<link>/api/projects/1/rate_project/`

Same endpoits applies to a local running app on localhost:

## Deployed version
> [API link](https://looku-awards.herokuapp.com/api/)



