from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from ML.call import get_excel
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "kuchtohhaibasye"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aryan2424@localhost/vidyutam'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.is_premium}')"
    

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6), EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user.id)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        user = User.query.filter_by(id=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html", form=form)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        if User.query.filter_by(id=username).first():
            flash("Username already exists!", "danger")
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(id=username, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))
    return render_template('register.html', form=form)

@app.route('/predict', methods=["GET", "POST"])
def predict():
    date1 = request.form.get("start_date")
    date2 = request.form.get("end_date")

    print(f"date1: {date1}\ndate2: {date2}")
    


    return render_template("dashboard.html")
    
@app.route('/get-predictions', methods=['GET'])
def get_predictions():
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        get_excel(start_date, end_date)

        df = pd.read_excel("Predictions.xlsx")

        df["Date"] = pd.to_datetime(df["Date"])  


        if not start_date or not end_date:
            return jsonify({"error": "Missing date parameters"})

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter data by date range
        df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

        if df_filtered.empty:
            return jsonify({"error": "No data available for selected range"})

        df_filtered["Month"] = df_filtered["Date"].dt.to_period("M")
        df_grouped = df_filtered.groupby("Month")["Electricity Required"].sum().reset_index()

        # Convert dataframe to JSON
        data = {
            "labels": df_grouped["Month"].astype(str).tolist(),
            "values": df_grouped["Electricity Required"].tolist(),
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/start')
def start():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
    
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)