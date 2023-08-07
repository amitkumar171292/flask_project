from flask import Flask, render_template, abort

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/<page_type>/")
def pages(page_type):
    if page_type in ["projects", "tasks", "users"]:
        return render_template(page_type + "/index.html")
    else:
        return abort(404)
  
if __name__ == "__main__":
    app.run(debug=True)
