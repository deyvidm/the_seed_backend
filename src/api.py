from src import app

@app.route("/")
@app.route("/index")
def index():
    return "balls"
