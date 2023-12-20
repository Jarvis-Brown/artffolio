from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Project:
    DB = "artfolio_schema"

    def __init__(self, project):
        self.id = project["id"]
        self.image = project["image"]
        self.title = project["title"]
        self.description = project["description"]
        self.file = project["file"]
        self.created_at = project["created_at"]
        self.updated_at = project["updated_at"]
        self.user = None
    
    @classmethod
    def get_one_by_id(cls, project_id):
        query = """SELECT * FROM projects
        JOIN users on projects.user_id = users.id
        WHERE projects.id = %(id)s;"""
    
        data = {
            "id": project_id
        }
        project_dict = connectToMySQL(cls.DB).query_db(query, data)[0]
        print(project_dict)
        
        project_obj = Project(project_dict)

        user_obj = user.User ({
            "id": project_dict["users.id"],
            "first_name": project_dict["first_name"],
            "last_name": project_dict["last_name"],
            "email": project_dict["email"],
            "password" : project_dict["password"],
            "created_at": project_dict["created_at"],
            "updated_at": project_dict["updated_at"]
        })
        project_obj.user = user_obj
        return project_obj
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM projects JOIN users ON users.id = projects.user_id;"""
        results = connectToMySQL(cls.DB).query_db(query)
        projects = []
        for project_dict in results:
            project_obj = Project(project_dict)
            user_obj = user.User({
                "id": project_dict["users.id"],
                "first_name": project_dict["first_name"],
                "last_name": project_dict["last_name"],
                "email": project_dict["email"],
                "password": project_dict["password"],
                "created_at": project_dict["created_at"],
                "updated_at": project_dict["updated_at"]
            })
            project_obj.user = user_obj
            projects.append(project_obj)
        return projects
    
#### Create Valid Project #####
    @classmethod
    def save(cls, project_data):
        query =  """
        INSERT INTO projects (user_id, image, title, description, file)
        VALUES (%(user_id)s,%(image)s, %(title)s, %(description)s, %(file)s);
        """
        connectToMySQL(cls.DB).query_db(query, project_data)
        return True
    
##### DELETE Project by ID #######
    @classmethod
    def delete_by_id(cls, project_id):
        query = """DELETE FROM projects
                WHERE id = %(id)s;"""
        data = {"id": project_id}
        connectToMySQL(cls.DB).query_db(query, data)
        return

    
##### Update Project ######
    @classmethod
    def update(cls, project_data):
        query = """UPDATE projects
        SET image = %(image)s, title = %(title)s, description = %(description)s, file = %(file)s
        WHERE id = %(id)s;"""
        connectToMySQL(cls.DB).query_db(query, project_data)
        return

####### Valid Method ######
    def is_valid(form_data, file_data):
        valid = True

        # Validate title
        if len(form_data.get("title", "")) == 0:
            valid = False
            flash("Title is required")

        # Validate description
        if len(form_data.get("description", "")) == 0:
            valid = False
            flash("Description is required")
        elif len(form_data.get("description")) < 3:
            valid = False
            flash("Description must be at least 3 characters")

        # Validate image file
        image_file = file_data.get('image') if 'image' in file_data else None
        if not image_file or image_file.filename == '':
            valid = False
            flash("Image is required")

        # Validate other file
        other_file = file_data.get('file') if 'file' in file_data else None
        if not other_file or other_file.filename == '':
            valid = False
            flash("File is required")

        return valid


    
    
    
    
