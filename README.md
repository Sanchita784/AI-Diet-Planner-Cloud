Project Overview
A Flask-based web application that helps users generate personalized diet plans based on their age and selected goal.
The application provides user registration, secure login, diet-plan generation, diet history, file uploads, cloud storage, and REST APIs.
The project demonstrates the integration of Python, Flask, SQLite, rule-based recommendations, REST APIs, and Cloudinary cloud storage. 

Problem Statement
Planning a suitable daily diet can be difficult for users who want simple recommendations based on their personal goals.
This project provides a web-based platform where users can select a goal, generate a personalized diet plan, save their diet history, and store related files in the cloud.

Key Features
User registration and login
Password hashing
Session-based authentication
Personalized rule-based diet recommendations
Goal-based diet generation
Diet history
File upload
Cloudinary cloud storage
Uploaded-file history
REST APIs
Protected API routes
File type and file-size validation
Environment-variable based configuration

How It Works
User
  |
  v
Flask Web Application
  |
  +----------------------+
  |                      |
  v                      v
Age + Goal          SQLite Database
  |                      |
  v                      +-- Users
Rule-Based               +-- Diet History
Recommendation            +-- File Records
Engine
  |
  v
Diet Plan

File Upload
  |
  v
Cloudinary
  |
  v
Cloud File Storage

Technology Stack
Programming Language: Python
Backend: Flask
Frontend: HTML, CSS
Database: SQLite
Cloud Storage: Cloudinary
Security: Werkzeug password hashing, Flask sessions
Configuration: python-dotenv
Version Control: Git and GitHub

Recommendation Engine
The project uses a rule-based recommendation engine implemented in Python.
The engine takes the useage and selected goal as inputs and generates a diet plan containing:
Breakfast
Lunch
Evening Snack
Dinner
The current implementation uses predefined rules rather than a machine-learning or generative-AI model.

Cloud Storage
Cloudinary is integrated for cloud-based file storage.
The application supports uploading:
PDF
JPG
JPEG
PNG
The application validates the file type and maximum file size before uploading.
After a successful upload, Cloudinary provides a secure URL that can be used to access the stored file.

Authentication & Database
Authentication
The application provides:
User registration
Login
Logout
Password hashing
Session-based authentication
Protected routes
Database
SQLite is used to store:
User information
Hashed passwords
User age
Diet history
Diet goals
Generated meals
Uploaded-file records
Cloud storage URLs

REST APIs
The application provides the following REST API endpoints:
/api/profile
/api/diet
/api/diet-history
/api/uploaded-files

The API routes are protected and require an authenticated user session.
Project Structure
AI-Diet-Planner-Cloud/
│
├── app.py
├── .gitignore
├── README.md
│
├── ai/
│   └── diet_generator.py
│
├── cloud/
│   └── cloudinary_config.py
│
├── database/
│   ├── db.py
│   └── api/
│       ├── __init__.py
│       ├── user_api.py
│       ├── diet_api.py
│       ├── diet_history_api.py
│       └── uploaded_files_api.py
│
└── templates/
    ├── index.html
    ├── register.html
    ├── login.html
    ├── dashboard.html
    ├── goal.html
    ├── diet.html
    ├── history.html
    ├── upload.html
    └── files.html
 Installation & Setup
Install the required dependencies:
pip install flask cloudinary python-dotenv werkzeug

Create a .env file in the project root:
FLASK_SECRET_KEY=your_secret_key
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

Do not upload the .env file to GitHub.
Run the application:
python app.py
Open the local URL displayed in the terminal.
and accessed through its generated URL.


Testing & Results
The following functionality has been tested successfully:
User registration
User login
Password validation
Dashboard access
Goal selection
Diet-plan generation
Diet history
File upload
Cloudinary cloud storage
Uploaded-file history
REST APIs
Protected routes
Logout
File type validation
File-size validation
The uploaded test file was successfully stored in Cloudinary and accessed through its generated URL.

Limitations & Future Improvements
Current Limitations
The recommendation engine is rule-based.
No machine-learning or generative-AI model is currently integrated.
SQLite is intended for local/small-scale usage.
The Flask application has not yet been deployed to a public cloud platform.
Diet recommendations are general and not medical advice.
Future Improvements
Integrate a genuine AI/ML recommendation model.
Add dietary preferences and activity level.
Add calorie and nutritional analysis.
Migrate to a production cloud database.
Deploy the Flask application to the cloud.
Add stronger API authentication.
Improve UI/UX.
Add automated testing.
