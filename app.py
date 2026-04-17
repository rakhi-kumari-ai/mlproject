from flask import Flask, request, render_template, flash, redirect
import os

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = Flask(__name__)
app.secret_key = "ml_project_secret_key"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        gender = request.form.get('gender')
        race = request.form.get('race_ethnicity')
        education = request.form.get('parental_level_of_education')
        lunch = request.form.get('lunch')
        test_course = request.form.get('test_preparation_course')
        reading_score = request.form.get('reading_score')
        writing_score = request.form.get('writing_score')

        # Validation
        if not all([gender, race, education, lunch, test_course, reading_score, writing_score]):
            flash("⚠️ Please fill all fields correctly!")
            return redirect('/')

        reading_score = int(reading_score)
        writing_score = int(writing_score)

        data = CustomData(
            gender=gender,
            race_ethnicity=race,
            parental_level_of_education=education,
            lunch=lunch,
            test_preparation_course=test_course,
            reading_score=reading_score,
            writing_score=writing_score
        )

        pred_df = data.get_data_as_data_frame()

        pipeline = PredictPipeline()
        result = pipeline.predict(pred_df)

        return render_template('home.html', results=round(result[0], 2))

    except Exception as e:
        flash(f"Error: {str(e)}")
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)