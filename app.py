import os
import importlib
import inspect
from flask import Flask, jsonify, request, abort
from classes.base_object import BaseObject

app = Flask(__name__)

def load_classes_from_directory(directory):
    classes = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]  # strip '.py'
            module_path = f"{directory}.{module_name}"
            module = importlib.import_module(module_path)
            # inspect each module member
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # we only want classes inheriting from BaseObject in our class modules
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
        obj = cls(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201

    # 👉 New explicit update route via HTTP PUT
    @app.route(f'/{endpoint}/<int:obj_id>', methods=['PUT'], endpoint=f'update_{endpoint[:-1]}')
    def update_object(obj_id, cls=cls):
        obj = cls.find_by_id(obj_id)
        if not obj:
            abort(404, description=f"{cls.__name__} with id {obj_id} not found")

        data = request.json
        # Update existing attributes explicitly:
        for key, value in data.items():
            obj.set_attribute(key, value)
        # Save updated object
        obj.save()
        return jsonify(obj.to_dict()), 200

# IMPORTANT: Ensure the directory is recognized as module (add empty __init__.py file)
classes = load_classes_from_directory('classes')

# clearly iterate over dynamically loaded classes to register flask routes
for cls in classes.values():
    register_routes_for_class(cls)

if __name__ == '__main__':
    app.run(debug=True, port=5000)