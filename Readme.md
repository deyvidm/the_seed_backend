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

###`tests`

This is where all of our unit testing will live. 
It is empty as of now, hopefully that will change :) 

###`db_repository` 

This directory is used by SQLAlchemy to keep backups and perform DB migrations.
We should not be writing any code that goes in there. 


