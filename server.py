import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)


# File configuration
UPLOAD_FOLDER = '/Users/filippovarini/Desktop/analyser/CVs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COUNT'] = 0


@app.route('/')
def hello_world():
    print("get request")
    return 'Hello world!'


@app.route('/cv-parse', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        answers = request.form.get('answers')
        name = request.form.get('name')
        team = request.form.get('team')
        print(answers, name, team)
        f = request.files['file']
        app.config['COUNT'] = app.config['COUNT'] + 1
        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], f'{app.config['COUNT']}{f.filename}'))
        return 'Thank you! Your data has been saved correctly!'


@app.route('/company-profile', methods=['GET', 'POST'])
def save_company_profiles():
    if request.method == 'POST':
        company = request.form.get('company')
        answers = request.form.get('answers')
        print(company, answers)
        return 'Thank you! Your data has been saved correctly!'


if __name__ == '__main__':
    print("hello")
    app.run()
