import os
from parse_cv import parse_cv
from scan_github import scan_github
from flask import Flask
from flask_pymongo import PyMongo
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import json
app = Flask(__name__)

load_dotenv()

#Db
CONNECTION_STRING = os.getenv("MONGO_URI")
print(CONNECTION_STRING)
mongodb_client = PyMongo(app, uri=CONNECTION_STRING)
db = mongodb_client.db


# File configuration
UPLOAD_FOLDER = '/Users/filippovarini/Desktop/analyser/CVs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COUNT'] = 0


@app.route('/')
def hello_world():
    print("get request")
    return 'Hello world!'

def save_file(file):
    app.config['COUNT'] = app.config['COUNT'] + 1
    count = app.config['COUNT']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{count}{file.filename}')
    file.save(filename)
    return filename


@app.route('/cv-parse', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        answers = request.form.get('answers')
        name = request.form.get('name')
        team = request.form.get('team')
        f = request.files['file']
        filename = save_file(f)
        company_score, language_score, buzzword_score, github_link = parse_cv(filename)
        experience, tech_stack, stars = scan_github(github_link.split('/')[-1])
        
        entry = {
            'name': name,
            'team': team,
            'answers': answers,
            'company_score': str(company_score), 
            'language_score': str(language_score), 
            'buzzword_score': str(buzzword_score), 
            'experience': str(experience),
            'stars': str(stars),
            'tech_stack': json.dumps(tech_stack)
        }

        print(entry)

        db.answers.insert_one(entry)

        return 'Thank you! Your data has been saved correctly!'


@app.route('/company-profile', methods=['GET', 'POST'])
def save_company_profiles():
    if request.method == 'POST':
        company = request.form.get('company')
        answers = request.form.get('answers')
        print(company, answers)
        return 'Thank you! Your data has been saved correctly!'

#test to insert data to the data base
@app.route("/test")
def test():
    print("testing")
    db.answers.insert_one({"name": "John", "team": "ell", "answers": "1010101111"})
    print("no")
    return "Connected to the data base!"


if __name__ == '__main__':
    print("hello")
    app.run()
