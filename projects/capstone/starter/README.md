# Full Stack Casting Agency app API Backend

## About
The Casting Agency app is used to show, store, update and delete Movies and Actors.
A user can send a post request with Movies and actors details in order to store these values. The user can also
retrieve these Movies and Actors . Further, the user can update the actors and movies details and
also delete any actor and movie by sending requests to the appropriate endpoints.

The endpoints and how to send requests to these endpoints for actors and movies are described in the 'Endpoint Library' section of the README.

All endpoints need to be tested using curl or postman since there is no frontend for the app yet.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

In the warranty-tracker directory, run the following to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

To run the server, execute:
```
python3 app.py
```
We can now also open the application via Heroku using the URL:
https://casting-agency2020.herokuapp.com/

The live application can only be used to generate tokens via Auth0, the endpoints have to be tested using curl or Postman 
using the token since I did not build a frontend for the application.

## DATA MODELING:
#### models.py
The schema for the database and helper methods to simplify API behavior are in models.py:
- There are two tables created: Actor and Movie
- The Actor table has primary key of an id , name , age and gender.
- The Actor table has insert,update, delete and formate functions 
- The Movie table has primary key of an id, title and release_date.
- The Movie has insert,update, delete and formate functions.


## API ARCHITECTURE AND TESTING
### Endpoint Library

@app.errorhandler decorators were used to format error responses as JSON objects. Custom @requires_auth decorator were used for Authorization based
on roles of the user. Three roles are assigned to this API: CASTING_ASSISTANT, CASTING_DIRECTOR and EXECUTIVE PRODUCER. 

CASTING_ASSISTANT role has the following permissions:
- retreive all actors and movies.

CASTING_DIRECTOR role has the following permission:
-retreive all actors and movies.
-add and delete actors .
-modify existing actors and movies.

EXECUTIVE PRODUCER role has the following permission:
-retreive all actors and movies.
-add and delete actors.
-modify existing actors and movies.
-add and delete movies.

A token needs to be passed to each endpoint. 

For the follwing endpoint, the token can be retrived by following these steps:
1. Go to https: https://azeezudacity.us.auth0.com/authorize?audience=http://localhost:8080/&response_type=token&client_id=SKGkKb36N290sybOuIdJcsAmJJ2spS2T&redirect_uri=https://casting-agency2020.herokuapp.com/

2. Then enter the following token:
   token: CASTING_ASSISTANT_TOKEN
   

#### GET '/ACTORS'
Returns a list of all available actors.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" https://casting-agency2020.herokuapp.com/actors 
Sample response output:
{
  "success": true,
  "actors": [
    {
      "id": "1",
      "name": "Peter Pan",
      "age": 31,
      "gender": "Male",
    }
  ]
}

#### GET '/MOVIES'
Returns a list of all available movies.
Sample curl: 
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" https://casting-agency2020.herokuapp.com/movies 
Sample response output:
{
  "success": true,
  "movies": [
    {
      "id": "1",
      "title": "Robinhood",
      "release_data": "Thu, 12 May 2016 00:00:00 GMT"
    }
  ]
}

For the follwing endpoint, the token can be retrived by following these steps:
1. Go to https: https://azeezudacity.us.auth0.com/authorize?audience=http://localhost:8080/&response_type=token&client_id=SKGkKb36N290sybOuIdJcsAmJJ2spS2T&redirect_uri=https://casting-agency2020.herokuapp.com/

2. Then enter the following token:
   token: CASTING_DIRECTOR_TOKEN

#### POST '/ACTORS'
Add new actor and Returns a the new actor that has been added.
Sample curl: 
curl https://casting-agency2020.herokuapp.com/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"Samoal John", "age": 22, "gender": "Male"}'
Sample response output:
{
  "success": True,
  "actor": 
    {
      "id": 2,
      "name": "Samoal John",
      "age": 22,
      "gender": "Male"
    }
}

#### PATCH '/actors/{actor_id}'
Update given actor and Returns the altered actor.
Sample curl:
curl https://casting-agency2020.herokuapp.com/actors/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"Canon Printer"}'
{
  "success": true,
  "actor": 
    {
      "id": 1,
      "name": "Canon Printer",
      "age": 31,
      "gender": "Male",
    }
}

#### PATCH '/movies/{movie_id}'
Update given movie and Returns the altered movie.
Sample curl:
curl https://casting-agency2020.herokuapp.com/movies/1 -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"title":"Home alone"}'
{
  "success": true,
  "actor": 
    {
      "id": 1,
      "title": "Home alone",
      "release_date": "Thu, 12 May 2016 00:00:00 GMT"
    }
}

#### DELETE '/actors/{actor_id}'
Delete and Returns the deleted actor.
curl https://casting-agency2020.herokuapp.com/actors/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" 
{
  "success": true,
  "actor": 
  {
      "id": 1,
      "name": "Canon Printer",
      "age": 31,
      "gender": "Male",
    }
}

For the follwing endpoint, the token can be retrived by following these steps:
1. Go to https: https://azeezudacity.us.auth0.com/authorize?audience=http://localhost:8080/&response_type=token&client_id=SKGkKb36N290sybOuIdJcsAmJJ2spS2T&redirect_uri=https://casting-agency2020.herokuapp.com/

2. Then enter the following token:
   token: EXECUTIVE PRODUCER_TOKEN

#### POST '/MOVIES'
Add new movie and Returns a the new movie that has been added.
Sample curl: 
curl https://casting-agency2020.herokuapp.com/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"title":"mission impossible", "release_date":"Thu, 12 May 2016 00:00:00 GMT"}'
Sample response output:
{
  "success": True,
  "movie": 
    {
      "id": 1,
      "title": "mission impossible",
      "release_date": "Thu, 12 May 2016 00:00:00 GMT"
    }
}

#### DELETE '/movies/{movie_id}'
Delete and Returns the deleted actor.
curl https://casting-agency2020.herokuapp.com/movies/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" 
{
  "success": true,
  "movie": 
  {
      "id": 1,
      "title": "home alone",
      "release_date": "Thu, 12 May 2016 00:00:00 GMT"
    }
}

## Testing
There are 16 unittests in test_app.py. To run this file use, change ENV = 'test' in config file and then run the following:
```
dropdb testCasting
createdb testCasting
python test_app.py
```
The tests include one test for expected success and error behavior for each endpoint, and tests demonstrating role-based access control, 
where all endpoints are tested with and without the correct authorization.

## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the 'user' and 'seller' roles.

## DEPLOYMENT
The app is hosted live on heroku at the URL: 
https://casting-agency2020.herokuapp.com/

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl or postman.
