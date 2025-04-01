"""
Dynamically Generated Flask REST API Server
This module provides a dynamically generated RESTful API using Flask, enabling CRUD (Create, Read, Update)
operations for all model classes inheriting from the BaseObject superclass. The application dynamically
discovers class implementations from the specified 'classes' directory structure.

Key functionalities:
- Dynamic class discovery from a dedicated directory ('classes')
- Automatic REST endpoint registration for CRUD operations per discovered class
- JSON-based object persistence without external dependencies or database migrations

Endpoints supported per discovered class:
- GET    /<classname>             List all objects of the class
- GET    /<classname>/<id>        Retrieve a single object by id
- POST   /<classname>             Create a new object of the given class
- PUT    /<classname>/<id>        Update an existing object by id

Dependencies:
- Flask
- Flask-Cors (CORS handling)

Usage:
    python app.py
"""
import importlib
import inspect
import os
from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from classes.base_object import BaseObject

app = Flask(__name__)
CORS(app)

def load_classes_from_directory(directory):
    """
    Lädt dynamisch alle Klassen aus dem angegebenen Ordner,
    die von BaseObject erben.
    """
    classes = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            module_path = f"{directory}.{module_name}"
            module = importlib.import_module(module_path)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseObject) and obj is not BaseObject:
                    classes[name] = obj
    return classes

def register_routes_for_class(cls):
    endpoint = cls.__name__.lower() + 's'

    @app.route(f'/{endpoint}', methods=['GET'], endpoint=f'get_all_{endpoint}')
    def list_objects(cls=cls):
        objs = cls.load_all()
        return jsonify(objs)

    @app.route(f'/{endpoint}/<int:obj_id>', methods=['GET'], endpoint=f'get_{endpoint[:-1]}')
    def get_object(obj_id, cls=cls):
        obj = cls.find_by_id(obj_id)
        if not obj:
            abort(404, description=f"{cls.__name__} not found")
        return jsonify(obj.to_dict())

    @app.route(f'/{endpoint}', methods=['POST'], endpoint=f'create_{endpoint[:-1]}')
    def create_object(cls=cls):
        data = request.json
        allowed_fields = set(inspect.signature(cls.__init__).parameters.keys())
        allowed_fields.discard('self')
        allowed_fields.discard('id')

        unknown_fields = set(data.keys()) - allowed_fields
        if unknown_fields:
            abort(400, description=f"Unbekannte Attribute erhalten: {', '.join(unknown_fields)}")
        try:
            obj = cls(**data)
            obj.save()
        except TypeError as e:
            abort(400, description=str(e))
        return jsonify(obj.to_dict()), 201

    @app.route(f'/{endpoint}/<int:obj_id>', methods=['PUT'], endpoint=f'update_{endpoint[:-1]}')
    def update_object(obj_id, cls=cls):
        obj = cls.find_by_id(obj_id)
        if not obj:
            abort(404, description=f"{cls.__name__} with id {obj_id} not found")
        data = request.json
        for key, value in data.items():
            obj.set_attribute(key, value)
        obj.save()
        return jsonify(obj.to_dict()), 200

@app.route('/problems_with_solutions', methods=['GET'], endpoint='fetch_problems_with_solutions')
def fetch_problems_with_solutions():
    from classes.problem import Problem
    from classes.problem_solution import ProblemSolution
    problems = Problem.load_all()

    for problem in problems:
        solution_ids = problem.get('problem_solution_ids', [])
        problem['problem_solutions'] = [
            ProblemSolution.find_by_id(s_id).to_dict() 
            for s_id in solution_ids 
            if ProblemSolution.find_by_id(s_id)
        ]
    return jsonify(problems)

# dynamisches Laden & Registrieren aller Klassen-Routen
classes = load_classes_from_directory('classes')
for cls in classes.values():
    register_routes_for_class(cls)

# Serverstart im Debug-Modus mit automatischem Reload
if __name__ == '__main__':
    app.run(debug=True, port=5000)