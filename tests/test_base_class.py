"""
Test suite for the BaseObject class.

Tests the key behaviors of BaseObject:
- Object Creation and initialization
- Dynamic attribute usage
- JSON persistence behavior (save/load explicitly)
- Object retrieval from persisted JSON storage via unique identifiers
"""

import pytest
import os
from classes.base_object import BaseObject

class TestObject(BaseObject):
    storage_file = 'test_object.json'

@pytest.fixture(autouse=True)
def clear_json_storage():
    """Fixture ensuring test json storage file gets cleared before and after each test."""
    test_file = TestObject.storage_file
    if os.path.exists(test_file):
        os.remove(test_file)
    yield
    if os.path.exists(test_file):
        os.remove(test_file)

def test_dynamic_attribute_access():
    """Test accessing dynamically set attributes on an instance."""
    obj = TestObject(custom_attr='value123')
    assert obj.custom_attr == 'value123'

def test_save_and_load():
    """Ensure objects can be correctly saved and re-loaded from JSON storage."""
    obj = TestObject(name='test_object')
    obj.save()
    all_objs = TestObject.load_all()
    assert len(all_objs := obj.load_all()) == 1  # Explicitly check that exactly one object was saved
    assert all_objs[0]['name'] == 'test_object'

def test_find_by_id():
    """Test retrieval of a saved object explicitly by its unique ID."""
    obj = TestObject(name='special_object')
    obj.save()
    found_obj = TestObject.find_by_id(obj.id)
    assert found_obj is not None
    assert found_obj.name == 'special_object'

def test_missing_storage_file_raises_error():
    """Check behavior explicitly when a subclass fails to define a storage file."""
    class NoStorageSubclass(BaseObject):
        pass

    test_obj = NoStorageSubclass(foo='bar')
    with pytest.raises(ValueError):
        test_obj.save()