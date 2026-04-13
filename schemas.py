from marshmallow import Schema, fields, validate

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=0))
    sets = fields.Int(validate=validate.Range(min=0))
    duration_seconds = fields.Int(validate=validate.Range(min=0))
    exercise = fields.Nested(ExerciseSchema, only=("name", "category"), dump_only=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(validate=validate.Range(min=1)) 
    notes = fields.Str()
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema, exclude=("workout_id",)))