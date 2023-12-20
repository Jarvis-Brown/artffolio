from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    def __init__(self, user):
        self.id = user['id']
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.email = user['email']
        self.password = user['password']
        self.created_at = user['created_at']
        self.updated_at = user['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s);"
        results = connectToMySQL('artfolio_schema').query_db(query,data)
        
        return results
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('artfolio_schema').query_db(query)
        users = []
        for row in results:
            users.append( cls(row))

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('artfolio_schema').query_db(query, data)
        return cls(results[0]) if results else None
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('artfolio_schema').query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return None
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": user["email"]}
        results = connectToMySQL('artfolio_schema').query_db(query, data)

        if results and len(results) >= 1:
            flash("Email already taken.", "register_flash")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email.")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters")
            is_valid = False
        if len(user['last_name']) <= 3:
            flash("Last name must be at least 3 characters")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 3 characters")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match")

        return is_valid
    
