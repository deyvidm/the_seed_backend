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
	The body contains a JSON object that defines a `username` and `password`<br>
	On success, a status code 201 is returned. The body of the response contains a JSON object with the newly added user <br>
	The password is hashed before being stored in the DB. Once it is hashed, we discard the original plain string password <br>

	Example:
	curl -i -X POST -H "Content-Type: application/json" -d '{"username":"mark","password":"ilovemark"}' http://127.0.0.1:5000/api/users
	
	HTTP/1.0 201 CREATED
	Content-Type: application/json
	Location: http://127.0.0.1:5000/api/users/1
	Content-Length: 25
	Server: Werkzeug/0.11.11 Python/2.7.10
	Date: Wed, 23 Nov 2016 20:27:55 GMT

	{
  		"username": "mark"
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
	On failure a status code 401 (unauthorized) is returned.

	Example:
	curl -u mark:ilovemark -i -X GET http://127.0.0.1:5000/api/token
	HTTP/1.0 200 OK
	Content-Type: application/json
	Content-Length: 160
	Server: Werkzeug/0.11.11 Python/2.7.10
	Date: Wed, 23 Nov 2016 20:49:33 GMT

	{
  		"duration": 600, 
  		"token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ3OTkzNDc3MywiaWF0IjoxNDc5OTM0MTczfQ.eyJpZCI6MX0.GmrfOOPkXgY5q0V6ykTONa-UPPBF8g4LDSMnfFI4ub8"
	}

	** This returns a token that can be used in place of sending `username` and `password` with each request **

- GET **/api/resource**

	Return a protected resource.<br>
	Authentication token is also checked here which is pretty dope. <br>
	On success a JSON object with data for authenticated user returned. <br>
	On failure, status code 401 (unauthorized) is returned.

	Example:
	curl -u mark:ilovemark -i -X GET http://127.0.0.1:5000/api/resource

	** This is valid because `username` and `password` match ** 
	HTTP/1.0 200 OK
	Content-Type: application/json
	Content-Length: 29
	Server: Werkzeug/0.11.11 Python/2.7.10
	Date: Wed, 23 Nov 2016 20:47:52 GMT

	{
  		"data": "Hello, mark!"
	}

	curl -u mark:idontlovemark -i -X GET http://127.0.0.1:5000/api/resource

	** This is not valid because you don't lovemark anymore **

	HTTP/1.0 401 UNAUTHORIZED
	Content-Type: text/html; charset=utf-8
	Content-Length: 19
	WWW-Authenticate: Basic realm="Authentication Required"
	Server: Werkzeug/0.11.11 Python/2.7.10
	Date: Wed, 23 Nov 2016 20:48:36 GMT

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
