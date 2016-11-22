from src import app

@app.route("/")
@app.route("/index")
def index():
    return '''
<html>
  <head>
    <title>Home Page</title>
  </head>

  <body>
    balls
    <img src="http://i284.photobucket.com/albums/ll36/Bigsteve87/Gifs/CleaningBowlingBalls.gif">
  </body>
</html>
''' 
