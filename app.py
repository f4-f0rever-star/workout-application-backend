from flask import Flask, request, make_response, jsonify
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
        workouts = Workout.query.all()
        return make_response(workouts_schema.dump(workouts), 200)
    
    elif request.method == 'POST':
        json_data = request.get_json()
        try:
            data = workout_schema.load(json_data)
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

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    json_data = request.get_json()
    new_we = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=json_data.get('reps'),
        sets=json_data.get('sets'),
        duration_seconds=json_data.get('duration_seconds')
    )
    db.session.add(new_we)
    db.session.commit()
    return make_response(workout_ex_schema.dump(new_we), 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)