from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)

def get_random_health_tip():
    tips = [
        "Stay hydrated!",
        "Exercise regularly!",
        "Eat a balanced diet!",
        "Get enough sleep!",
        "Manage your stress levels!"
    ]
    return random.choice(tips)

def analyze_vitals(age, sex, bp_sys, bp_dia, hr, temp, pain, symptoms, preexisting, family_history):
    score = 0
    issues = []

    if bp_sys > 130 or bp_dia > 80:
        issues.append("Possible Hypertension")
        score += 2
    if hr < 60 or hr > 100:
        issues.append("Possible Abnormal Heart Rate")
        score += 2
    if temp > 100.4:
        issues.append("Possible Fever or Infection")
        score += 2
    if pain >= 7:
        issues.append("High Pain Level")
        score += 2

    if "Chest Pain" in symptoms or "Shortness of Breath" in symptoms:
        issues.append("Possible Cardiac Issue")
        score += 3
    if "Fainting" in symptoms or "Dizziness" in symptoms:
        issues.append("Possible Neurological Issue")
        score += 2
    if "Nausea" in symptoms and temp > 99:
        issues.append("Possible Gastrointestinal Issue")
        score += 1

    if "Diabetes" in preexisting:
        issues.append("Higher Risk: Diabetes")
        score += 1
    if "Heart Disease" in preexisting:
        issues.append("Higher Risk: Heart Disease")
        score += 2

    if "Stroke" in family_history:
        score += 1
    if "Cancer" in family_history:
        score += 1

    if score >= 6:
        advice = "Seek immediate medical attention."
    elif score >= 3:
        advice = "Consult a physician soon."
    else:
        advice = "Vitals are acceptable. Monitor symptoms."

    return advice, issues, score

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        age = int(data['age'])
        sex = data['sex']
        bp_sys = int(data['bp_sys'])
        bp_dia = int(data['bp_dia'])
        hr = int(data['hr'])
        temp = float(data['temp'])
        pain = int(data['pain'])
        symptoms = data.getlist('symptoms')
        custom_symptom = data['custom_symptom']
        if custom_symptom:
            symptoms.append(custom_symptom)

        preexisting = data.getlist('preexisting')
        family_history = data.getlist('family_history')

        advice, issues, score = analyze_vitals(age, sex, bp_sys, bp_dia, hr, temp, pain, symptoms, preexisting, family_history)
        tip = get_random_health_tip()

        # Save submission to database
        conn = sqlite3.connect('health.db')
        c = conn.cursor()
        c.execute('''INSERT INTO submissions (date, age, sex, bp_sys, bp_dia, hr, temp, pain, symptoms, advice)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (datetime.now(), age, sex, bp_sys, bp_dia, hr, temp, pain, ', '.join(symptoms), advice))
        conn.commit()
        conn.close()

        return render_template('result.html', advice=advice, issues=issues, tip=tip, score=score)

    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    c.execute('SELECT name FROM symptoms')
    symptoms = [row[0] for row in c.fetchall()]

    c.execute('SELECT name FROM preexisting_conditions')
    conditions = [row[0] for row in c.fetchall()]

    c.execute('SELECT name FROM family_history')
    histories = [row[0] for row in c.fetchall()]
    conn.close()

    return render_template('index.html', symptoms=symptoms, conditions=conditions, histories=histories)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    c.execute('SELECT * FROM submissions ORDER BY date DESC')
    submissions = c.fetchall()
    conn.close()
    return render_template('dashboard.html', submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True)
