**🛡️ Cyber Threat Detection Web App**

This is a Flask-based Intrusion Detection System (IDS) Web Application that uses a Random Forest Classifier to classify network traffic or system events into different categories of cyber threats.

**The app provides:**

🔐 User authentication (Sign Up & Login) with SQLite

📊 Dashboard views (Dataset, Intrusion Detection, Executive Dashboard)

📂 File upload for prediction

🤖 Machine Learning-based prediction of threats

📉 Confusion Matrix visualization

⭐ Feature importance visualization

🚀 Features


**User Management**

Signup with unique email

Login & authentication system (SQLite database)

Threat Prediction

Upload a .csv dataset with the required features

Preprocessing with a pre-trained Scaler

Classification using a pre-trained Random Forest Classifier

Percentage distribution of predicted threat categories

Visualization

Confusion Matrix heatmap

Top 10 Feature Importances (Bar chart)

**Threat Categories**  
  
  Benign
  Adware
  Riskware
  Trojan
  Ransomware


**🛠️ Tech Stack**

Backend: Flask, SQLite

Machine Learning: Scikit-learn (Random Forest Classifier)

Visualization: Matplotlib, Seaborn

Frontend: HTML templates, Bootstrap/CSS

Other: Flask-CORS, Joblib, Pandas

**📂 Project Structure**

├── app.py                # Main Flask application

├── ai_models/            # ML models and features

│   ├── random_forest_Classifier.pkl

│   ├── scaler.pkl

│   └── features.txt

├── templates/            # HTML templates (login, signup, dashboard, etc.)

├── static/               # Static files (CSS, JS, images)

├── users.db              # SQLite database for user management

**⚙️ Installation & Setup**

Clone the repository

git clone https://github.com/muhammadwaqas1564/Machine-Learning-for-Predicting-Cyber-Threats.git
cd cyber-threat-detection


**Create a virtual environment & activate it**

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


**Install dependencies**

pip install -r requirements.txt


**Run the Flask app**

python app.py


**Open your browser at:**

http://127.0.0.1:5000/

**📊 Input Format for Prediction**

Upload a CSV file containing the selected features listed in ai_models/features.txt.

The file must also include a Class column for validation.

Example (first few rows):

feature1,feature2,feature3,...,Class
0.12,0.45,0.78,...,1
0.34,0.67,0.89,...,4

**📸 Screenshots**

Login Page

Dashboard

Confusion Matrix Heatmap

Feature Importance Graph

**👨‍💻 Author**

Developed by Muhammad Waqas
