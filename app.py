from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from sklearn.metrics import confusion_matrix
from collections import Counter
import matplotlib.pyplot as plt
from flask_cors import CORS
import seaborn as sns
import pandas as pd
import matplotlib
import sqlite3
import joblib
import base64
import io
import os



# -------------------------> Load ML models
model = joblib.load("ai_models/random_forest_Classifier.pkl")
scaler = joblib.load("ai_models/scaler.pkl")
with open("ai_models/features.txt", "r") as f:
    selected_features = (f.readline()).split(',')

# -------------------------> Label mapping
label_mapping = {
    1: "Benign",
    2: "Adware",
    3: "Riskware",
    4: "Trojan",
    5: "Ransomware"
}

# -------------------------> Flask setup
app = Flask(__name__, template_folder='templates', static_folder='Static')
CORS(app)

# ----------------------------------- Database Setup ----------
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def insert_user(self, name, email, password):
        self.cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        self.conn.commit()

    def get_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        return self.cursor.fetchone()

db = Database()

# ----------------------------------- Routes ----------
@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

@app.route('/intrusiondetection')
def intrusiondetection():
    return render_template('intrusiondetection.html')

@app.route('/executivedashboard')
def executivedashboard():
    return render_template('executivedashboard.html')


@app.route('/')
def root():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match")
        try:
            db.insert_user(name, email, password)
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('signup.html', error="Email already registered")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.get_user_by_email(email)

        if not user:
            return render_template('login.html', error="User not registered")
        if password != user[3]:
            return render_template('login.html', error="Incorrect password")
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    df = pd.read_csv(file)
    missing = [f for f in selected_features if f not in df.columns]
    if missing:
        return jsonify({"error": "Missing required features"}), 400

    X = df[selected_features]
    y = df['Class']
    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)

    result = {
        label_mapping.get(cls, str(cls)): round((count / len(y_pred)) * 100, 2)
        for cls, count in Counter(y_pred).items()
    }

    cm = confusion_matrix(y, y_pred)
    labels = list(label_mapping.values())
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, cmap="Blues", fmt="d", xticklabels=labels, yticklabels=labels)
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    confusion_image = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    plt.close()

    importances = model.feature_importances_
    feature_df = pd.DataFrame({'Feature': selected_features, 'Importance': importances})
    top_features = feature_df.sort_values(by='Importance', ascending=False).head(10)
    plt.figure(figsize=(6, 5))
    sns.barplot(data=top_features, x="Importance", y="Feature", palette="Blues_d")
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    feature_image = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    plt.close()

    return jsonify({
        "result": result,
        "confusion_matrix": confusion_image,
        "feature_importance": feature_image
    })

# ---------------------------------- Run Server ----------
if __name__ == '__main__':
    app.run(debug=True)
