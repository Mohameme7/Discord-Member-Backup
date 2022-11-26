import flask, sqlite3, httpx
app = flask.Flask(__name__,template_folder="html")

@app.route('/')
def main():
    return