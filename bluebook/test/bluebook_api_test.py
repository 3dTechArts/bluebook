#!/usr/bin/env python3
"""
BlueBook API Test Module

This module contains the unit tests for the BlueBook API functionality.
It uses the `unittest` framework to define and execute the test cases.

The test cases cover various functions of the BlueBook API, including adding a contact,
removing a contact, updating a contact, searching for contacts, exporting the phonebook,
and retrieving a target contact.

Each test case is defined as a method within the `BlueBookApiTestCase` class, which is
a subclass of `unittest.TestCase`.

To execute the tests, run this module as the main script.

Author: Reza Mousavi
Date: May 10, 2023
"""

import unittest
import os
import sys
import io
from datetime import datetime
from unittest.mock import patch, mock_open
import argparse

from lib.person import Person
from lib.phonebook import Phonebook
from api.bluebook import *


class BlueBookApiTestCase(unittest.TestCase):
    """
    Test case class for the BlueBook API.

    This class defines test cases for the various functions of the BlueBook API.

    Methods:
        setUp: Method called before each test case to set up the test environment.
        test_get_target_contact: Test case for the get_target_contact function.
        test_add_contact: Test case for the add_contact function.
        test_remove_contact: Test case for the remove_contact function.
        test_update_contact: Test case for the update_contact function.
        test_search_contacts: Test case for the search_contacts function.
        test_export_phonebook: Test case for the export_phonebook function.
    """

    def setUp(self):
        """
        Method called before each test case to set up the test environment.

        This method instantiates a phonebook instance and creates a StringIO object
        to capture the output. It also redirects stdout to the StringIO object.
        """
        self.phonebook = Phonebook()
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    @patch('builtins.input', return_value='yes')
    def test_get_target_contact(self, mock_input):
        """
        Test case for the get_target_contact function.

        This test case verifies the behavior of the get_target_contact function by
        setting up test data, calling the function under test, and asserting the result.

        It uses the patch decorator to mock the built-in input function and provide
        a predetermined user input.

        Test steps:
        1. Set up test data.
        2. Call the function under test.
        3. Assert the result.

        Args:
            mock_input: Mocked input function.

        Returns:
            None.
        """
        name_info = ['John', 'Doe']
        contact = Person(first_name='John', last_name='Doe', phone='123456', address='123 Main St')
        self.phonebook.add_contact(contact)
        result = get_target_contact(name_info, self.phonebook)
        self.assertEqual(result, contact)

    def test_add_contact(self):
        """
        Test case for the add_contact function.

        This test case verifies the behavior of the add_contact function by setting up
        test data, calling the function under test, and asserting the result.

        Test steps:
        1. Set up test data.
        2. Call the function under test.
        3. Assert the contact is added to the phonebook.

        Returns:
            None.
        """
        args = argparse.Namespace(first_name='John', 
                                  last_name='Doe', 
                                  phone='123456', 
                                  address='123 Main St')
        
        add_contact(args, self.phonebook)
        self.assertEqual(len(self.phonebook.contacts), 1)
        self.assertEqual(self.phonebook.contacts[0].first_name, 'John')
        self.assertEqual(self.phonebook.contacts[0].last_name, 'Doe')
        self.assertEqual(self.phonebook.contacts[0].phone, '123456')
        self.assertEqual(self.phonebook.contacts[0].address, '123 Main St')

    @patch('builtins.input', return_value='yes')
    def test_remove_contact(self, mock_input):
        """
        Test case for the remove_contact function.

        This test case verifies the behavior of the remove_contact function by setting up
        test data, calling the function under test, and asserting the result.

        It uses the patch decorator to mock the built-in input function and provide
        a predetermined user input.

        Test steps:
        1. Set up test data.
        2. Call the function under test.
        3. Assert the contact is removed from the phonebook.

        Args:
            mock_input: Mocked input function.

        Returns:
            None.
        """
        args = argparse.Namespace(remove=['John', 'Doe'])
        phonebook = Phonebook()
        contact = Person(first_name='John', last_name='Doe', phone='123456', address='123 Main St')
        phonebook.add_contact(contact)
        remove_contact(args, phonebook)
        self.assertEqual(len(phonebook.contacts), 0)

    @patch('builtins.input', return_value='yes')
    def test_update_contact(self, mock_input):
        """
        Test case for the update_contact function.

        This test case verifies the behavior of the update_contact function by setting up
        test data, calling the function under test, and asserting the result.

        It uses the patch decorator to mock the built-in input function and provide
        a predetermined user input.

        Test steps:
        1. Set up test data.
        2. Call the function under test.
        3. Assert the contact is updated in the phonebook.

        Args:
            mock_input: Mocked input function.

        Returns:
            None.
        """
        args = argparse.Namespace(
            update=['John', 'Doe'],
            phone='9876543210',
            first_name='John',
            last_name='Mcenzy',
            address='1235 new way'
        )

        contact = Person(first_name='John', last_name='Doe', phone='123456', address='123 Main St')
        self.phonebook.add_contact(contact)
        update_contact(args, self.phonebook)
        self.assertEqual(len(self.phonebook.contacts), 1)
        self.assertEqual(self.phonebook.contacts[0].phone, '9876543210')

    def test_search_contacts(self):
        """
        Test case for the search_contacts function.

        This test case verifies the behavior of the search_contacts function by setting up
        test data, calling the function under test, and asserting the result.

        Test steps:
        1. Set up test data.
        2. Call the function under test.
        3. Assert the search result.

        Returns:
            None.
        """
        args = argparse.Namespace(search=['John', 'Doe'])
        person1 = Person(first_name='John', last_name='Doe', phone='123456', address='123 Main St')
        person2 = Person(first_name='Jane', last_name='Smith', phone='987654', address='456 Elm St')
        self.phonebook.add_contact(person1)
        self.phonebook.add_contact(person2)
        result = search_contacts(args, self.phonebook)
        self.assertEqual(len(result), 1)
        self.assertIn(person1, result)

    def test_export_phonebook(self):
        """
        Test case for the export_phonebook function.

        This test case verifies the behavior of the export_phonebook function by setting up
        test data, calling the function under test, and asserting the result.

        Test steps:
        1. Set up test data.
        2. Set up mock file and export format.
        3. Patch the built-in open function.
        4. Patch the datetime module to return a fixed timestamp.
        5. Call the function under test.
        6. Assert that the open function was called with the expected filename and mode.

        Returns:
            None.
        """
        person1 = Person(first_name='John', last_name='Doe', phone='123456', address='123 Main St')
        person2 = Person(first_name='Jane', last_name='Smith', phone='987654', address='456 Elm St')
        self.phonebook.add_contact(person1)
        self.phonebook.add_contact(person2)

        export_format = 'json'
        mock_file = mock_open()

        with patch('builtins.open', mock_file) as mock_open_file:
            fixed_timestamp = '2023-05-11_00-03-48'  # Update with the actual timestamp generated during the test
            with patch('datetime.datetime') as mock_datetime:
                mock_datetime.now.return_value = datetime.strptime(fixed_timestamp, '%Y-%m-%d_%H-%M-%S')

                expected_filename = export_phonebook(self.phonebook, export_format)
                expected_filepath = os.path.join('exports', expected_filename)
                print('expected_filepath', expected_filepath)
                mock_open_file.assert_called_once_with(expected_filepath, 'w')


if __name__ == '__main__':
    unittest.main()

