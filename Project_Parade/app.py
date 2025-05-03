from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file, send_from_directory
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from config import Config
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import zipfile
import json
import pickle
from mapping import *
import numpy as np
import pandas as pd
import requests
import MySQLdb.cursors

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# File Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
PROJECTS_FILE = os.path.join(app.root_path, 'static', 'projects.json')


# Folder where uploaded projects will be stored
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    
# Loading a pre-trained Decision Tree (DT) model using pickle
with open(r"C:\Users\HARSH\Desktop\Project_Parade\dt_model.pkl", 'rb') as model_file:
    model = pickle.load(model_file)
    
    
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        

@app.route('/')
def outer_page():
    return render_template('outer.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # Use DictCursor
        cursor.execute("SELECT * FROM user WHERE username=%s", [username])
        user = cursor.fetchone()
        cursor.close()

        if user:
            if bcrypt.check_password_hash(user['password'], password_candidate):
                session['logged_in'] = True
                session['username'] = user['username']  # Corrected key
                session['email'] = user['email']  # Corrected key
                session['user_id'] = user['id']  # Corrected key
                
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password', 'password_error')
        else:
            flash('Username not found', 'username_error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        cursor = mysql.connection.cursor()
        
        # Checking if the email already exists
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Email already taken.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match.', 'error')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
            mysql.connection.commit()
            flash('You have successfully registered! Please log in.', 'success')
            cursor.close()
            return redirect(url_for('login'))
        
        cursor.close()

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        username = session.get('username', 'Student')  # Default to 'Student' if not found
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('login'))
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(r'C:\Users\HARSH\Desktop\Project_Parade\uploads', filename)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Insert data into MySQL database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact (name, email, subject, message) VALUES (%s, %s, %s, %s)",
                    (name, email, subject, message))
        mysql.connection.commit()
        cur.close()

        # Flash a success message
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        # Get updated values from form
        updated_username = request.form['name']
        updated_email = request.form['email']

        # Update session values
        session['username'] = updated_username
        session['email'] = updated_email

        # Update database
        cursor.execute("UPDATE user SET username = %s, email = %s WHERE id = %s", 
                       (updated_username, updated_email, user_id))
        mysql.connection.commit()
        flash('Profile updated successfully!', 'success')

    # Fetch user data from database to ensure persistence
    cursor.execute("SELECT username, email FROM user WHERE id = %s", (user_id,))
    student = cursor.fetchone()
    cursor.close()

    return render_template('profile.html', student=student)


@app.route('/project_pool', methods= ['GET'])
def project_pool():
    return render_template('project_pool.html')


# Function to check if a file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_paper', methods=['POST'])
def upload_paper():
    title = request.form['paper-title']
    
    if 'paper-file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('research_papers'))

    file = request.files['paper-file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('research_papers'))

    if file and allowed_file(file.filename):
        # Save the file
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        flash('Paper uploaded successfully!', 'success')

    return redirect(url_for('research_papers'))

@app.route('/research_papers')
def research_papers():
    papers = []
    # Fetch all PDF and DOCX files from the upload directory
    for filename in os.listdir(UPLOAD_FOLDER):
        if allowed_file(filename):
            papers.append({
                'title': filename,
                'filename': filename,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
    return render_template('research_papers.html', papers=papers)

# Use your actual research papers for suggestions
research_papers = [
    {"title": "2024_ProjectHubCollaborativePlatformforStudentandFaculties", "filename": "2024_ProjectHubCollaborativePlatformforStudentandFaculties.pdf", "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"title": "chef_tool", "filename": "chef_tool.pdf", "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"title": "Enhance Capstone Projects with a New Online Collaboration System", "filename": "Enhance Capstone Projects with a New Online Collaboration System.pdf", "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"title": "Innovative Online Platforms Research Opportunities", "filename": "Innovative Online Platforms Research Opportunities.pdf", "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"title": "my-resume", "filename": "my-resume.pdf", "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    {"title": "SCM", "filename": "SCM.pdf", "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
]


@app.route('/get_paper_suggestions', methods=['GET'])
def get_paper_suggestions():
    query = request.args.get('q', '').lower()
    
    # Filter papers that match the query string
    matching_papers = [paper for paper in research_papers if query in paper['title'].lower()]

    return jsonify(matching_papers)

# Load existing projects
def load_projects():
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save projects
def save_projects(projects):
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=4)

@app.route('/global_projects')
def global_projects():
    projects = load_projects()
    return render_template('global_projects.html', projects=projects)

@app.route('/upload_project', methods=['POST'])
def upload_project():
    if request.method == 'POST':
        project_title = request.form.get('projectTitle')
        uploaded_by = request.form.get('uploadedBy')
        college = request.form.get('college')
        upload_date = datetime.today().strftime('%Y-%m-%d')

        files = request.files.getlist('projectFiles')

        project_folder = os.path.join(UPLOAD_FOLDER, project_title.replace(" ", "_"))
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)

        file_links = []
        for file in files:
            filename = file.filename
            file_path = os.path.join(project_folder, filename)
            file.save(file_path)
            file_links.append(url_for('static', filename=f'uploads/{project_title.replace(" ", "_")}/{filename}', _external=True))

        new_project = {
            "title": project_title,
            "uploaded_by": uploaded_by,
            "college": college,
            "upload_date": upload_date,
            "files": file_links
        }

        projects = load_projects()
        projects.append(new_project)
        save_projects(projects)

        return jsonify({"message": "Project uploaded successfully!", "projects": projects})

@app.route('/download_project/<project_title>')
def download_project(project_title):
    project_folder = os.path.join(UPLOAD_FOLDER, project_title.replace(" ", "_"))
    zip_filename = f"{project_title.replace(' ', '_')}.zip"
    zip_filepath = os.path.join(UPLOAD_FOLDER, zip_filename)

    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        for filename in os.listdir(project_folder):
            zipf.write(os.path.join(project_folder, filename), arcname=filename)

    return send_file(zip_filepath, as_attachment=True)


@app.route('/prediction')
def prediction():
    return render_template('prediction.html')


@app.route('/predict_project', methods=['POST'])
def predict_project():
    if request.method == "POST":
        # Parse incoming JSON data
        data = request.get_json()
        
        # Extract skills from the request, defaulting to 'No Skill' if not provided
        skills = [
            data.get('skill1', 'html'),
            data.get('skill2', 'html'),
            data.get('skill3', 'html'),
            data.get('skill4', 'html')
        ]
        
        encoded_skills = []
        for idx, skill in enumerate(skills, start=1):
         column = f'skill{idx}'
         encoded_value = skills_mapping.get(column, {}).get(skill, -1)  # Fixing skill lookup
         encoded_skills.append(encoded_value)

        
        # If all skills are invalid (encoded as 0), return an error response
        if all(value == 0 for value in encoded_skills):
            return jsonify({
                'project': 'Invalid Skills',
                'description': ''   # Empty description as no valid skills were provided
            })
        
        # Create a DataFrame to make a prediction
        user_input_df = pd.DataFrame([encoded_skills], columns=['skill1', 'skill2', 'skill3', 'skill4'])
        
        try:
            # Predict the project using the pre-trained model
            model_output = model.predict(user_input_df)[0]
            print(f"Model Output: {model_output}")  # Debug output
            
            # Convert model output to an integer if it's not already
            if isinstance(model_output, (np.int64, float, np.float64)):
                model_output = int(model_output)  # Convert to integer
            
            # Map model output to the project name
            predicted_project = project_mapping.get(model_output, "Unknown Project")
            print(f"Predicted Project after mapping: {predicted_project}")
        
        except Exception as e:
            print(f"Prediction error: {e}")
            predicted_project = "Error during prediction"
        
        # Return prediction results
        return jsonify({
            'project': predicted_project,
            'description': "This project is recommended based on your skills."  # Placeholder description
        })


@app.route('/more_project_suggestions', methods=['POST'])
def more_project_suggestions():
    data = request.get_json()
    skills = data.get('skills', '')

    payload = {
    "model": "gemma2:2b",
    "prompt": (
        f"Generate 5 unique project ideas using the following skills: {skills}. "
        "Format each idea as:\n\n"
        "[Project Title]: [Brief description in 1-2 sentences]\n\n"
        "Ensure the title and description are clearly separated. Do not include extra formatting, numbers, or section titles."
    ),
    "stream": False
}

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response_data = response.json()
        
        # Extract response and clean up the format
        raw_suggestions = response_data.get("response", "").strip()
        projects = [idea.strip() for idea in raw_suggestions.split("\n\n") if idea.strip()]

        return jsonify({"suggestions": projects})

    except Exception as e:
        print(f"Error fetching suggestions from Ollama: {e}")
        return jsonify({"suggestions": ["❌ Error fetching project suggestions from the API"]})



if __name__ == '__main__':
    app.run(debug=True)
