from app import app

@app.route("/")
def index():
    return '<html><h1 style="text-align: center;">Hello World from Flask!</h1></html>'