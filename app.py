from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = ""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True)