# Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

## Motivation
This is a Casting Agency Capstone Project requierd for Udacity Full Stack Web Developer Nanodegree Program.

This project covers: 
- Data modeling using `postgres`.
- API development and testing using `Flask`.
- Authentication using `Auth0`.
- Authorization with `Role-Based Access Control`.
- API deployment using `Heroku`.

## Dependencies

### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight SQLite database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. 

#### Python
Install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Environment
This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies:
`pip install -r requirements.txt`
This will install all of the required packages we selected within the `requirements.txt` file.

### Running the server
Each time you open a new terminal session, run: `FLASK_APP=app.py`
To run the server, execute:`flask run --reload`

The `--reload` flag will detect file changes and restart the server automatically.

## API Endpoints
- Actors
    - GET `/actors`
    - POST `/actors`
    - PATCH `/actors/int:id`
    - DELETE `/actors/int:id`
- Movies
    -  GET `/movies`
    -  POST `/movies`
    -  PATCH `/movies/int:id`
    -  DELETE `/movies/int:id`

## Permissions
Role-Based Access Control was applied in this project. Thus, there are three type of users: 
- Casting Assistant can:
    - Actor
        -  GET `/actors`
    - Movie
        -  GET `/movies`

-  Casting Director can:
    - Actor
        -   GET `/actors`
        -   POST `/actors`
        -   PATCH `/actors/int:id`
        -   DELETE `/actors/int:id`
    - Movie
        -   GET `/movies`
        -   PATCH `/movies/int:id`    
                
- Executive Producer can:
    - Actor
        -   GET `/actors`
        -   POST `/actors`
        -   PATCH `/actors/int:id`
        -   DELETE `/actors/int:id`
    - Movie
        -   GET `/movies`
        -   POST `/movies`
        -   PATCH `/movies/int:id`  
        -   DELETE `/movies/int:id` 

## Live API

This app uses Auth0 as Authentication provider. JWTs for different role can be accessed by login to the link with the credential provided below https://ta0.us.auth0.com/authorize?audience=castingagency&response_type=token&client_id=YLeo1NWxEi3yLpyZd0abi3s6bg1S6DV4&redirect_uri=https://127.0.0.1:5000/actors


### Authentication information:

- Casting Assistant:
    - User: `casting_assistant@test.test`
    - Password: `casting_assistant1234`
- Casting Director:
    - User: `casting_director@test.test`
    - Password: `casting_director1234`
- Executive Producer
    - User: `executive_producer@test.test`
    - Password: `executive_producer1234`

Test the endpoints with the following link: https://castingagency448.herokuapp.com/ useing cURL command 


## API Endpoints Documentation
### API Endpoints Behaviors

#### GET /actors
- Description: Return a list of all actors with details from the Database
- cURL command: Curl -i -X GET -H "Authorization: Bearer ${TOKEN}" https://castingagency448.herokuapp.com/actors
- Example Response:

```
{
    "Actors": [
                {
                    "age":25,
                    "id":2,
                    "name":"leen"
                }
    ],
    "success":true
}
```
#### GET /movies
- Description: Return a list of all movies from the Database
- cURL command: Curl -i -X GET -H "Authorization: Bearer ${TOKEN}" https://castingagency448.herokuapp.com/movies
- Example Response:
```
{
    "Movies": [
                {
                    "id":1,
                    "releas date":"Tue, 12 Dec 2023 00:00:00 GMT",
                    "title":"good time"
                }
    ],
"success": true
}
```
#### POST /actors
- Description: Insert a new actor into the Database
- cURL command:  Curl -i -X POST -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type:application/json" -d "{$requset body}" https://castingagency448.herokuapp.com/actors
- Request body example :
```
{            
    "name": "Leen",
    "age": 27,
    "gender": "Female"
}
```
- Example cURL: `Curl -i -X POST -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type:application/json" -d "{\"name\":\"leen\",\"age\":"23",\"gender\":\"female\"}" https://castingagency448.herokuapp.com/actors`
- Example Response:
```
{
    "actor": [
                {
                "actor":"leen",
                }
    ],
    "success": true
}
```
#### POST /movies

- Description: Create a new Movie, Insert a new movie into the Database
- cUrl command: Curl -i -X POST -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type:application/json" -d "{$requset body}" https://castingagency448.herokuapp.com/movies
- Request body example :

```
{
    "title": "Good time",
    "release_date": "1-1-2020"
}
```
- Example cURL:`Curl -i -X POST -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type:application/json" -d "{\"title\":\"good time\", \"release_date \": \"12-12-2023 \"}" https://castingagency448.herokuapp.com/movies`
- Example Response:
```
{
    " Movie ": [
                {
                "Good time"
                }
    ],
    "success": true
}
```

#### PATCH /movies/<int:id>

- Description: Update an existing Movie details
- Request argument: ID - Movie ID 
- cURL command: Curl -i -X PATCH -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type:application/json" -d "{$Requset_body}" https://castingagency448.herokuapp.com/actors/$id
- Request body example : the title or the release date, Any or Both of these fields can be updated

```
{
    "title": "Good Life"      
}
```
- Ecample cURL: `Curl -i -X PATCH -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type:application/json" -d "{\"age\":25}"  https://castingagency448.herokuapp.com/actors/1`
- Example Response:
```
{
    "movie": [
                {
                "Good Life"
                }
                ],
    "success": true
}
```

#### PATCH /actors/<int:id>

- Description: Update an existing Actor's Details using the Actor's ID
- Request argument: ID - Actor ID - 1
-  cURL command: Curl -i -X PATCH -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type:application/json" -d "{$Requset_body}" https://castingagency448.herokuapp.com/movies/$id
- Request Body : The Name or the Age or the Gender, any or all of them can be updated
```
{
    "age": 20
}
```
- EXAMPLE cURL:Curl -i -X PATCH -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type:application/json" -d "{\"title\":\"good life ,good time\"}"  https://castingagency448.herokuapp.com/movies/1
- Example Response:

```
{
    "actor": [
                {
                "name":"leen"
                }
    ],
    "success": true
}

```

#### DELETE /actors/<int:id>

- Description: Delete an existing Actor using the Actor's ID
- Request argument: ID - Actor ID - 1
- curl command:Curl -i -X DELETE -H "Authorization: Bearer ${TOKEN}" https://castingagency448.herokuapp.com/actors/$id
- Request Body : None

- example cURL: `Curl -i -X DELETE -H "Authorization: Bearer ${TOKEN}" https://castingagency448.herokuapp.com/actors/1` 
- Example Response:
```
{
    "actor": leen was successfuly deleted",
    "success":true
}
```

#### DELETE /movies/<int:id>

- Description: Delete an existing Movie using the Movie's ID
- Request argument: ID - Movie ID - 1
- Request Body : None
- curl command:Curl -i -X DELETE -H "Authorization: Bearer ${TOKEN}" https://castingagency448.herokuapp.com/actors/1

- EXample cURL: `Curl -i -X DELETE -H "Authorization: Bearer ${TOKEN}" https://castingagency448.herokuapp.com/movies/1  `
- Example Response:
```
{
    " Movie":"Good life was successfuly deleted”,
    "success":true
}
```

## Reference
https://auth0.com/docs/quickstart/backend/python/01-authorization
