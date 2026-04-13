from flask import Flask, request, make_response
from flask_migrate import Migrate
from models import db, Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_ex_schema = WorkoutExerciseSchema()

@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'GET':
        return make_response(workouts_schema.dump(Workout.query.all()), 200)
    elif request.method == 'POST':
        try:
            data = workout_schema.load(request.get_json())
            new_workout = Workout(**data)
            db.session.add(new_workout)
            db.session.commit()
            return make_response(workout_schema.dump(new_workout), 201)
        except Exception as e:
            return make_response({"errors": str(e)}, 400)

@app.route('/workouts/<int:id>', methods=['GET', 'DELETE'])
def workout_by_id(id):
    workout = Workout.query.get_or_404(id)
    if request.method == 'GET':
        return make_response(workout_schema.dump(workout), 200)
    elif request.method == 'DELETE':
        db.session.delete(workout)
        db.session.commit()
        return make_response({}, 204)

@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'GET':
        return make_response(exercises_schema.dump(Exercise.query.all()), 200)
    elif request.method == 'POST':
        try:
            data = exercise_schema.load(request.get_json())
            new_exercise = Exercise(**data)
            db.session.add(new_exercise)
            db.session.commit()
            return make_response(exercise_schema.dump(new_exercise), 201)
        except Exception as e:
            return make_response({"errors": str(e)}, 400)

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    Workout.query.get_or_404(workout_id)
    Exercise.query.get_or_404(exercise_id)
    
    try:
        data = workout_ex_schema.load(request.get_json())
        new_we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            **data
        )
        db.session.add(new_we)
        db.session.commit()
        return make_response(workout_ex_schema.dump(new_we), 201)
    except Exception as e:
        return make_response({"errors": str(e)}, 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)