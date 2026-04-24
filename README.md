# workout-application-backend
A RESTful backend API for workout tracking used by personal trainers. Built with Flask, SQLAlchemy, and Marshmallow.

The workout tracker supports full CRUD operations for workouts and exercises to workouts with performance metadata.

# Instructions
1. Clone the repository
git clone git@github.com:f4-f0rever-star/workout-application-backend.git
2. Install dependencies with Pipenv
pipenv install
* **Virtual environment**
pipenv shell
4. Initialize and run database migrations
export FLASK_APP=app.py
flask db init
flask dn migrate -m "comment"
flask db upgrade
5. Seed the database
python3 seed.py
# Run instructions
python3 app.py