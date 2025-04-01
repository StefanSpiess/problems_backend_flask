import json
import os
from datetime import datetime

class BaseObject:
    storage_file = None  # subclasses must override this!

    def __init__(self, id=None, **kwargs):
        self._attributes = kwargs
        if id is not None:
            self._attributes['id'] = id

    def set_attribute(self, key, value):
        self._attributes[key] = value

    def get_attribute(self, key, default=None):  
        return self._attributes.get(key, default)

    def __getattr__(self, key):
        try:
            return self._attributes[key]
        except KeyError:
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{key}'")

    def __setattr__(self, key, value):
        if key in ('_attributes', 'storage_file'):
            super().__setattr__(key, value)
        else:
            self._attributes[key] = value

    def to_dict(self):
        return self._attributes

    def save(self):
        if self.storage_file is None:
            raise ValueError("Subclass must define storage_file.")

        self._attributes['updated_at'] = datetime.now().isoformat()
        all_objs = self.load_all()

        if 'id' not in self._attributes:
            self._attributes['id'] = self._next_id(all_objs)

        for index, obj in enumerate(all_objs):
            if obj.get('id') == self._attributes['id']:
                all_objs[index] = self._attributes
                break
        else:
            all_objs.append(self._attributes)

        with open(self.storage_file, 'w') as f:
            json.dump(all_objs, f, indent=4)

    @classmethod
    def load_all(cls):
        """
        Load all stored instances of the current class from its corresponding JSON file.

        Returns:
            list[dict]: List of dictionaries, each representing a stored instance.
                        Returns an empty list if no stored objects exist.

        Raises:
            ValueError: If 'storage_file' has not been defined in the subclass.
        """
        if cls.storage_file is None:
            raise ValueError("Subclass must define storage_file.")
        if not os.path.exists(cls.storage_file):
            return []
        with open(cls.storage_file, 'r') as f:
            return json.load(f)

    @classmethod
    def find_by_id(cls, obj_id):
        """
        Find and return an object by its unique identifier.

        Args:
            obj_id (int): The unique identifier of the object to retrieve.

        Returns:
            BaseObject | None: An instance of the class (derived from BaseObject) matching the provided ID,
                            or None if no such object exists.
        """
        data = next((obj for obj in cls.load_all() if obj.get('id') == obj_id), None)
        return cls.from_dict(data) if data else None

    @classmethod
    def _next_id(cls, objects):
        """
        Determine the next available unique numeric identifier based on existing objects.

        Args:
            objects (list[dict]): List of existing stored objects used to calculate the next ID.

        Returns:
            int: The next free ID (current maximum ID + 1).
                Returns 1 if no existing IDs are found.
        """
        existing_ids = [obj.get('id', 0) for obj in objects if isinstance(obj.get('id'), int)]
        return max(existing_ids or [0]) + 1

    @classmethod
    def from_dict(cls, dict_data):
        """
        Instantiate an object of the class based directly on provided dictionary data,
        bypassing the standard __init__ constructor.

        Args:
            dict_data (dict): Dictionary containing all attributes of the object.

        Returns:
            BaseObject | None: A fully initialized class instance with attributes directly set,
                            or None if dict_data is None.
        """
        if dict_data is None:
            return None
        obj = cls.__new__(cls)
        setattr(obj, '_attributes', dict_data)
        return obj