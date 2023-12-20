from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.project import Project
from werkzeug.utils import secure_filename
import os

from flask_app import app

##### GET ROUTES #######
@app.route("/projects/home")
def projects_home():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/log")
    
    if "user_id" in session:
        user_id = session['user_id']
        print("User ID in session:", user_id)
    
    data={
        'id': session['user_id']
    } 
    
    user = User.get_by_id(data)

    projects = Project.get_all()

#### Get project info and send to template
    for project in projects:
        print("project.id", project.id)
        print("project.user.id", project.user.id)
    
    return render_template("home.html", user=user, projects=projects)

##### May not need to show Render Info and Detail Page

#### Create page #####
@app.route('/projects/new')
def create_page():
    return render_template('add_project.html')


##### Edit / Delete page ######
@app.route('/projects/edit/<project_id>')
def edit_project(project_id):
    project = Project.get_one_by_id(project_id)
    return render_template('edit.html', project=project)

@app.route('/projects/delete/<project_id>')
def delete_project(project_id):
    Project.delete_by_id(project_id)
    return redirect('/projects/home')

##### PROCESS FORMS ########

##### Create Process Form #####
def save_uploaded_file(file):
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        # Calculate the relative path to the upload folder based on the current working directory
        upload_folder = os.path.join(app.root_path, 'static', 'upload')
        full_path = os.path.join(upload_folder, filename)

        # Check if the directory exists, if not, create it
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file.save(full_path)
        return filename
    return None

def save_uploaded_image(image):
    if image and image.filename != '':
        filename = secure_filename(image.filename)
        # Calculate the relative path to the image upload folder based on the current working directory
        upload_folder = os.path.join(app.root_path, 'static', 'upload')
        full_path = os.path.join(upload_folder, filename)

        # Check if the directory exists, if not, create it
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        image.save(full_path)
        return filename
    return None

@app.route('/projects', methods=['POST'])
def add_project():
    # Extract file and image data from request.files
    uploaded_file = request.files.get('file')
    uploaded_image = request.files.get('image')

    # Check if the form data is valid (passing all file data)
    if not Project.is_valid(request.form, request.files):
        return redirect('/projects/new')

    project_data = request.form.to_dict()  # Convert form data to a mutable dictionary

    # Handle file upload
    file_filename = save_uploaded_file(uploaded_file)
    if file_filename:
        project_data['file'] = file_filename  # Add the file info to the project data
    else:
        flash("No file uploaded.")

    # Handle image upload
    image_filename = save_uploaded_image(uploaded_image)
    if image_filename:
        project_data['image'] = image_filename  # Add the image info to the project data
    else:
        flash("No image uploaded.")

    if not file_filename or not image_filename:
        return redirect('/projects/new')  # Redirect if either file or image upload failed

    Project.save(project_data)
    return redirect('/projects/home')

#### Update Process #####
@app.route('/projects/update', methods=["POST"])
def update_project():
    # Extract file and image data from request.files
    uploaded_file = request.files.get('file')
    uploaded_image = request.files.get('image')

    # Check if the form data is valid (passing all file data)
    if not Project.is_valid(request.form, request.files):
        return redirect(f"/projects/edit/{request.form['id']}")

    project_data = request.form.to_dict()  # Convert form data to a mutable dictionary

    # Handle file and image updates if provided
    file_filename = save_uploaded_file(uploaded_file)
    if file_filename:
        project_data['file'] = file_filename

    image_filename = save_uploaded_image(uploaded_image)
    if image_filename:
        project_data['image'] = image_filename

    Project.update(project_data)
    return redirect("/projects/home")
