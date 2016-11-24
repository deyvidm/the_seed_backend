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

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world<br>

We will be using this tutorial to grind our way through flask. <br>
You can skip the Templating and Web Forms, but be VERY sure to read the Database. <br>

We are using SQLAlchemy, which is a really awesome Object wrapper. <br>
Instead of making you work with raw SQL calls, SQLAlchemy works with classes<br>
which represent our tables. <br>

###`src/api.py`<br>

This is where all the endpoints live for now. As our API expands, we will <br>
need to create new files. <br>
Please be sure to update the Readme and tests! <br>

- GET **/api/product**

	Will receive a JSON string of all the results from the scraper from all time. <br>
	Returns 500 on Failure. <br>
	Returns 200 on Sucess and the following body: <br> 
	
	```JSON
	{
		"product name": [
		    {
		      "date": "date and time scraped", 
		      "food_id": 1, 
		      "food_name": "product_name", 
		      "location_id": 1, 
		      "location_name": "name of store", 
		      "price": price
		    }, 
		    {
		      "date": "date and time scraped", 
		      "food_id": 1, 
		      "food_name": "product name", 
		      "location_id": 2, 
		      "location_name": "name of second store", 
		      "price": price
		    }, 
		    {
		      "date": "date and time scraped", 
		      "food_id": 1 
		      "food_name": "product name", 
		      "location_id": 3, 
		      "location_name": "name of third store", 
		      "price": price
		    }
		],
		"different product name": [
		    {
		      "date": "date and time scraped", 
		      "food_id": 2 
		      "food_name": "different product name", 
		      "location_id": 1, 
		      "location_name": "name of store", 
		      "price": price
		    }
		]
	}
	```

- GET **/api/product/product_id**

	Will receive a JSON string of all the entries for a product with id product_id from all time. <br>
	Returns 204 on Failure. <br>
	Return 200 on Success and the following body: <br>
	
	```JSON
	{
		[
		    {
		      "date": "date and time scraped", 
		      "food_id": 0, 
		      "food_name": "product name", 
		      "location_id": 1, 
		      "location_name": "name of store", 
		      "price": price
		    }
		]
	}
	```

- POST **/api/scrape**

	Manually activate the scraper and fetch new data. <br> 
	User must be logged in to succeed. <br>
	Returns 500 on Failure. <br> 
	Returns 204 on Success. <br>

- POST **/api/users**

	Register a new user. <br>
	The body contains a JSON object that defines a `username` and `password`.<br>
	On success, a status code 201 is returned. The body of the response contains a JSON object with the newly added user. <br>
	The password is hashed before being stored in the DB. Once it is hashed, we discard the original plain string password. <br>

	Example: <br>
	```$ curl -i -X POST -H "Content-Type: application/json" -d '{"username":"mark","password":"ilovemark"}' http://127.0.0.1:5000/api/users```
	
	HTTP/1.0 201 CREATED <br>
	Content-Type: application/json <br>
	Location: http://127.0.0.1:5000/api/users/1 <br>
	Content-Length: 25 <br>
	Server: Werkzeug/0.11.11 Python/2.7.10 <br>
	Date: Wed, 23 Nov 2016 20:27:55 GMT <br>

	```JSON
	{ 
   		"username": "mark"
	}
	```

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
	```$ curl -u mark:ilovemark -i -X GET http://127.0.0.1:5000/api/token``` <br>
	
	HTTP/1.0 200 OK <br>
	Content-Type: application/json <br>
	Content-Length: 160 <br>
	Server: Werkzeug/0.11.11 Python/2.7.10 <br>
	Date: Wed, 23 Nov 2016 20:49:33 GMT <br>

	```JSON
	{ 
		"duration": 600,
		"token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ3OTkzNDc3MywiaWF0IjoxNDc5OTM0MTczfQ.eyJpZCI6MX0.GmrfOOPkXgY5q0V6ykTONa-UPPBF8g4LDSMnfFI4ub8" 
	}
	```

	**This returns a token that can be used in place of sending `username` and `password` with each request** <br>

- GET **/api/resource**

	Return a protected resource.<br>
	Authentication token is also checked here which is pretty dope. <br>
	On success a JSON object with data for authenticated user returned. <br>
	On failure, status code 401 (unauthorized) is returned. <br>

	Example: <br>
	```$ curl -u mark:ilovemark -i -X GET http://127.0.0.1:5000/api/resource``` <br>

	**This is valid because `username` and `password` match** <br>
	HTTP/1.0 200 OK <br>
	Content-Type: application/json <br>
	Content-Length: 29 <br>
	Server: Werkzeug/0.11.11 Python/2.7.10 <br>
	Date: Wed, 23 Nov 2016 20:47:52 GMT <br>

	```JSON
	{ 
		"data": "Hello, mark!"
	}
	```

	```$ curl -u mark:idontlovemark -i -X GET http://127.0.0.1:5000/api/resource``` <br>

	**This is not valid because you don't lovemark anymore** <br>

	HTTP/1.0 401 UNAUTHORIZED <br>
	Content-Type: text/html; charset=utf-8 <br>
	Content-Length: 19 <br>
	WWW-Authenticate: Basic realm="Authentication Required" <br>
	Server: Werkzeug/0.11.11 Python/2.7.10 <br>
	Date: Wed, 23 Nov 2016 20:48:36 GMT <br>

	Unauthorized Access

###`tests`

Testing is being completed through Postman. Postman is super cool and allows for clean testing of API endpoints.

All tests live in the tests/ folder. Inside there is a file called `API.postman_collection.json`.

Postman can be downloaded from: **https://www.getpostman.com**

Once downloaded:

1. Click `import` on the top left corner of the application.
2. Import the `API.postman_collection.json` file.
3. Once imported, click on the 'Collections' option in the top left and **API** should be visible as a collection.
4. Click the arrow to the right of the collection and a blue button named `Run` becomes visible.
5. Click on `Run` and all of the tests in the suite will be run and output how many tests are passed.

Shortcomings:

1. Testing creation of new and existing users is problematic as once the 'User New Creation' test is run once, the user <br>
is stored in the database and that test is no longer valid. At this point it is then run as a 'User Old Creation' test.

###`db_repository` 

This directory is used by SQLAlchemy to keep backups and perform DB migrations.
We should not be writing any code that goes in there. 

###Database

`./db_create.py` to create a database
`./fromScraper.py scraped.json` to populate the database
