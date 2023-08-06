from flask import Flask, render_template, abort

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/<page>/")
def pages(page):
    if page in ["projects", "tasks", "users"]:
        return render_template(page + "/index.html")
    else:
        return abort(404)
  
if __name__ == "__main__":
    app.run(debug=True)
