from app import app
from models import db, Workout, Exercise, WorkoutExercise
from datetime import date

with app.app_context():
    print("Clearing database...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    ex1 = Exercise(name="Squats", category="Legs", equipment_needed=True)
    db.session.add(ex1)
    
    print("Seeding workout...")
    w1 = Workout(date=date.today(), duration_minutes=60, notes="Morning session")
    db.session.add(w1)
    
    db.session.commit()
    print("Done!")