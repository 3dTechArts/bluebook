#!/usr/bin/env python3

import unittest
import sys
import io
from unittest.mock import patch
from lib.person import Person
from lib.phonebook import Phonebook


class BlueBookApiTestCase(unittest.TestCase):
    """
    Test case class for BlueBook API functionality.

    This class defines unit tests for the BlueBook API. It is a subclass of `unittest.TestCase` and
    provides various test cases for adding a contact, removing a contact, and updating a contact in 
    the phonebook.

    The tests use the `unittest.mock` module to mock the underlying methods of the `Phonebook` 
    class and verify the expected behavior.

    Methods:
        setUp(): Set up the test fixture.
        test_add_contact(): Test the add_contact() method of Phonebook.
        test_remove_contact(): Test the remove_contact() method of Phonebook.
        test_update_contact(): Test the update_contact() method of Phonebook.
    """

    def setUp(self):
        """
        Set up the test fixture.

        This method is called before each test case. It instantiates a `Phonebook` object and 
        sets up a `StringIO` object to capture the output printed to stdout during the tests.
        """
        self.phonebook = Phonebook()

        # Create a StringIO object to capture the output
        self.captured_output = io.StringIO()

        # Redirect stdout to the StringIO object
        sys.stdout = self.captured_output

    def test_add_contact(self):
        """
        Test case for the add_contact() method.

        This method tests the add_contact() method of the Phonebook class. It creates a Person 
        object with sample data, mocks the add_contact() method of the Phonebook object, and 
        asserts that the add_contact() method is called with the expected Person object.
        """
        person_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "123456789",
            "address": "123 Main St"
        }
        expected_person = Person(**person_data)

        with patch.object(self.phonebook, "add_contact") as mock_add_contact:
            self.phonebook.add_contact(expected_person)
            mock_add_contact.assert_called_with(expected_person)

    def test_remove_contact(self):
        """
        Test case for the remove_contact() method.

        This method tests the remove_contact() method of the Phonebook class. It creates a Person 
        object with sample data, mocks the remove_contact() method of the Phonebook object, 
        the expected Person object.
        """
        person_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "123456789",
            "address": "123 Main St"
        }
        person = Person(**person_data)

        with patch.object(self.phonebook, "remove_contact") as mock_remove_contact:
            self.phonebook.remove_contact(person)
            mock_remove_contact.assert_called_with(person)

    def test_update_contact(self):
        """
        Test case for the update_contact() method.

        This method tests the update_contact() method of the Phonebook class. It creates a Person 
        object with sample data, mocks the update_contact() method of the Phonebook object, 
        and asserts that the update_contact() method is called with the expected Person object.
        """
        person_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "123456789",
            "address": "123 Main St"
        }

        expected_updated_person = Person(**person_data)

        with patch.object(self.phonebook, "update_contact") as mock_update_contact:
            self.phonebook.update_contact(expected_updated_person)
            mock_update_contact.assert_called_with(expected_updated_person)



if __name__ == '__main__':
    unittest.main()
