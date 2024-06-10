#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
storage_type = os.environ.get('HBNB_TYPE_STORAGE')
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        error_message = "Found code style errors (and warnings)."
        self.assertEqual(result.total_errors, 0, error_message)

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        error_message = "Found code style errors (and warnings)."
        self.assertEqual(result.total_errors, 0, error_message)

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))


@unittest.skipIf(storage_type == 'db', 'skip if environ is not db')
class TestStorageGet(unittest.TestCase):
    """
    Testing `get()` method in DBStorage
    """

    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        print('\n\n.................................')
        print('...... Testing Get() Method ......')
        print('.......... Place  Class ..........')
        print('.................................\n\n')

    def setUp(self):
        """
        setup method
        """
        self.state = models.state.State(name="Florida")
        self.state.save()

    def test_get_method_obj(self):
        """
        testing get() method
        :return: True if pass, False if not pass
        """
        storage = FileStorage()
        print(self.state.id)
        result = storage.get(cls="State", id=self.state.id)

        self.assertIsInstance(result, models.state.State)

    def test_get_method_return(self):
        """
        testing get() method for id match
        :return: True if pass, false if not pass
        """
        storage = FileStorage()
        result = storage.get(cls="State", id=str(self.state.id))

        self.assertEqual(self.state.id, result.id)

    def test_get_method_none(self):
        """
        testing get() method for None return
        :return: True if pass, false if not pass
        """
        storage = FileStorage()
        result = storage.get(cls="State", id="doesnotexist")
        self.assertIsNone(result)


@unittest.skipIf(storage_type == 'db', 'skip if environ is not db')
class TestStorageCount(unittest.TestCase):
    """
    tests count() method in DBStorage
    """

    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        print('\n\n.................................')
        print('...... Testing Get() Method ......')
        print('.......... Place  Class ..........')
        print('.................................\n\n')

    def setup(self):
        """
        setup method
        """
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()

    def test_count_all(self):
        """
        testing counting all instances
        :return: True if pass, false if not pass
        """
        storage = FileStorage()
        result = storage.count()

        self.assertEqual(len(storage.all()), result)

    def test_count_state(self):
        """
        testing counting state instances
        :return: True if pass, false if not pass
        """
        storage = FileStorage()
        result = storage.count(cls="State")

        self.assertEqual(len(storage.all("State")), result)

    def test_count_city(self):
        """
        testing counting non existent
        :return: True if pass, false if not pass
        """
        storage = FileStorage()
        result = storage.count(cls="City")

        self.assertEqual(
            int(0 if len(storage.all("City")) is None else
                len(storage.all("City"))), result)
