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
- Flask (for RESTful API endpoints handling)

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
    Load and dynamically import all classes inheriting from BaseObject in
    the specified directory.

    This function iterates through Python files (.py) in the given directory,
    dynamically imports them as modules, and extracts class definitions that
    explicitly subclass from BaseObject.

    Args:
        directory (str): The name of the directory (as module path) containing the Python class files.

    Returns:
        dict: A mapping (class name to class object) containing all classes inheriting from BaseObject
              that have been dynamically imported from the directory.

    Raises:
        ImportError: If class module import fails due to syntax errors or incorrect module paths.
    """
    classes = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]  # strip '.py'
            module_path = f"{directory}.{module_name}"
            module = importlib.import_module(module_path)
            # Iterate over members and pick subclasses of BaseObject
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseObject) and obj is not BaseObject:
                    classes[name] = obj
    return classes

def register_routes_for_class(cls):
    """
    Dynamically register standard REST CRUD endpoints for the provided class.

    Registers HTTP endpoints for retrieving all objects, retrieving one object by ID,
    creating a new object, and updating an existing object by ID. Standard HTTP methods
    GET, POST, and PUT are used consistently across endpoints. All endpoints support and
    expect application/json payloads.

    Args:
        cls (type): Class object inheriting from BaseObject for which RESTful
                    CRUD routes should be created.

    Returns:
        None
    """
    endpoint = cls.__name__.lower() + 's'

    @app.route(f'/{endpoint}', methods=['GET'], endpoint=f'get_all_{endpoint}')
    def list_objects(cls=cls):
        """Fetch and return all persisted objects of the class as JSON."""
        objs = cls.load_all()
        return jsonify(objs)

    @app.route(f'/{endpoint}/<int:obj_id>', methods=['GET'], endpoint=f'get_{endpoint[:-1]}')
    def get_object(obj_id, cls=cls):
        """Fetch and return one persisted object by id. Return 404 if not found."""
        obj = cls.find_by_id(obj_id)
        if not obj:
            abort(404, description=f"{cls.__name__} not found")
        return jsonify(obj.to_dict())

    @app.route(f'/{endpoint}', methods=['POST'], endpoint=f'create_{endpoint[:-1]}')
    def create_object(cls=cls):
        data = request.json

        # Prüfe auf unbekannte Felder:
        allowed_fields = set(inspect.signature(cls.__init__).parameters.keys())
        allowed_fields.discard('self')
        allowed_fields.discard('id')  # id darf optional vom Client weggelassen werden

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
        """
        Update attributes explicitly for existing persisted object identified by id.

        Return the updated object as JSON. If object with specified id does not exist,
        return a 404 status code and clear error message.
        """
        obj = cls.find_by_id(obj_id)
        if not obj:
            abort(404, description=f"{cls.__name__} with id {obj_id} not found")
        data = request.json
        for key, value in data.items():
            obj.set_attribute(key, value)
        obj.save()
        return jsonify(obj.to_dict()), 200

# IMPORTANT: Ensure the directory ('classes') is initialized as a valid Python package with an empty __init__.py
classes = load_classes_from_directory('classes')

# Register routes explicitly for each dynamically loaded BaseObject subclass
for cls in classes.values():
    register_routes_for_class(cls)

if __name__ == '__main__':
    app.run(debug=True, port=5000)