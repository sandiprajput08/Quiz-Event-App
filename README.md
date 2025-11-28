# Quiz Events Django App

## Overview
A Django web application where users can view quizzes and events, attempt quizzes with dynamic questions, submit answers, and view results. Includes user authentication and a quiz history page showing logged-in users' past submissions.

## Tech Stack
- Python 3.x (core language)
- Django (backend)
- SQLite (database)
- Tailwind CSS (via CDN)
- Optional: Django REST Framework (installed)

## Features
- List all quizzes
- Start and attempt quizzes with dynamic MCQ/Text questions
- Submit answers, calculate score, and store submissions
- View detailed quiz results
- Browse upcoming events
- User signup/login/logout
- Quiz History page (shows user’s old submissions)
- Django Admin panel to create quizzes, questions, answers, and events



## Setup 

### 1. Create Virtual Environment :

- python -m venv venv
- source venv/bin/activate         # Linux/Mac
- venv\Scripts\activate            # Windows

### 2. Install Dependencies :

- pip install -r requirements.txt
  
### 3.  Apply Migrations :

-  python manage.py migrate
  
### 4. Create Admin User :

- python manage.py createsuperuser

 ### 5. Start Development Server :

 - python manage.py runserver

