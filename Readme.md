#Install

###Mac
`sudo easy_install virtualenv`

###Linux
`sudo apt-get install python-virtualenv`

###Windows 
`pip install virutalenv`

###after virutalenv is installed
```
virutalenv flask

flask/bin/pip install -r dependencies.txt
```

#Tutorial

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

We will be using this tutorial to grind our way through flask. 
You can skip the Templating and Web Forms, but be VERY sure to read the Database. 

We are using SQLAlchemy, which is a really awesome Object wrapper. 
Instead of making you work with raw SQL calls, SQLAlchemy works with classes
which represent our tables. 

###`src/api.py`

This is where all the endpoints live for now. As our API expands, we will 
need to create new files. 
Please be sure to update the Readme and tests! 

- POST **/api/users**

	Register a new user. <br>
	The body contains a JSON object that defines a `username` and `password`.<br>
	On success, a status code 201 is returned. The body of the response contains a JSON object with the newly added user. <br>
	The password is hashed before being stored in the DB. Once it is hashed, we discard the original plain string password. <br>

	Example: <br>
	$ curl -i -X POST -H "Content-Type: application/json" -d '{"username":"mark","password":"ilovemark"}' http://127.0.0.1:5000/api/users
	
	HTTP/1.0 201 CREATED <br>
	Content-Type: application/json <br>
	Location: http://127.0.0.1:5000/api/users/1 <br>
	Content-Length: 25 <br>
	Server: Werkzeug/0.11.11 Python/2.7.10 <br>
	Date: Wed, 23 Nov 2016 20:27:55 GMT <br>

	{ <br>
        "username": "mark" <br>
	}

- GET **/api/users/&lt;int:id&gt;**

	Returns a single user. <br>
	On success a status code of 200 is returned. The body of the response contains a JSON object with the requested user. <br>
	On failure, a status code of 400 (bad request) is returned

- GET **/api/token**

	Return an authentication token. <br>
	Useful for not having to pass `username` and `password` with every request. <br>
	On success a JSON object is returned with a field `token` set to authentication token for the user and a field `duration` set to 
	how long the token is valid for. <br>
	On failure a status code 401 (unauthorized) is returned. <br>

	Example: <br>
	$ curl -u mark:ilovemark -i -X GET http://127.0.0.1:5000/api/token <br>
	
	HTTP/1.0 200 OK <br>
	Content-Type: application/json <br>
	Content-Length: 160 <br>
	Server: Werkzeug/0.11.11 Python/2.7.10 <br>
	Date: Wed, 23 Nov 2016 20:49:33 GMT <br>

	{ <br>
        "duration": 600, <br>
        "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ3OTkzNDc3MywiaWF0IjoxNDc5OTM0MTczfQ.eyJpZCI6MX0.GmrfOOPkXgY5q0V6ykTONa-UPPBF8g4LDSMnfFI4ub8" <br>
	}

	**This returns a token that can be used in place of sending `username` and `password` with each request** <br>

- GET **/api/resource**

	Return a protected resource.<br>
	Authentication token is also checked here which is pretty dope. <br>
	On success a JSON object with data for authenticated user returned. <br>
	On failure, status code 401 (unauthorized) is returned. <br>

	Example: <br>
	$ curl -u mark:ilovemark -i -X GET http://127.0.0.1:5000/api/resource <br>

	**This is valid because `username` and `password` match** <br>
	HTTP/1.0 200 OK <br>
	Content-Type: application/json <br>
	Content-Length: 29 <br>
	Server: Werkzeug/0.11.11 Python/2.7.10 <br>
	Date: Wed, 23 Nov 2016 20:47:52 GMT <br>

	{ <br>
        "data": "Hello, mark!" <br>
	}

	$ curl -u mark:idontlovemark -i -X GET http://127.0.0.1:5000/api/resource <br>

	**This is not valid because you don't lovemark anymore** <br>

	HTTP/1.0 401 UNAUTHORIZED <br>
	Content-Type: text/html; charset=utf-8 <br>
	Content-Length: 19 <br>
	WWW-Authenticate: Basic realm="Authentication Required" <br>
	Server: Werkzeug/0.11.11 Python/2.7.10 <br>
	Date: Wed, 23 Nov 2016 20:48:36 GMT <br>

	Unauthorized Access

###`tests`

This is where all of our unit testing will live. 
It is empty as of now, hopefully that will change :) 

###`db_repository` 

This directory is used by SQLAlchemy to keep backups and perform DB migrations.
We should not be writing any code that goes in there. 

###Database

`./db_create.py` to create a database
`./populate.py` to populate the database
