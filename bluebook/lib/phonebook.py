"""
This module provides the Phonebook class for managing a collection of contacts.
It allows adding, removing, updating, and searching contacts.
Contacts are represented as instances of the Person class.

Module: phonebook.py
Author: Reza Mousavi (reza.mousavii@gmail.com)


Classes:
    - Phonebook: A class representing a phonebook, containing a list of Person objects.

Usage:
    1. Create a new Phonebook instance.
    2. Add contacts using the `add_contact()` method.
    3. Remove contacts using the `remove_contact()` method.
    4. Update contacts using the `update_contact()` method.
    5. Get all contacts using the `get_contacts()` method.
    6. Save the phonebook data to a file using the `save_to_file()` method.
    7. Load phonebook data from a file using the `load_from_file()` method.
    8. Search for contacts using the `search_contacts()` method.
    9. Display contact information using the `display_contact_info()` method.

Dependencies:
    - json: Required for serialization and deserialization in JSON format.
    - yaml: Required for serialization and deserialization in YAML format.
    - typing: Required for type hints.
            "typing: Required for type hints," means that the typing module is necessary 
            to define and use type hints in the Phonebook module. It clarifies that if you
            want to use the type hints provided in the module, you need to import the typing
            module. By using the types from the typing module, you can enhance the code's
            readability and help tools analyze the code more effectively

Note:
    The `Person` class and `styling` module from `config.baseconfig` are used within this module.

Example:
    from phonebook import Phonebook
    from person import Person
    from config.baseconfig import styling

    # Create a new phonebook
    pb = Phonebook()

    # Add a contact
    person = Person('John', 'Doe', '123-456-7890')
    pb.add_contact(person)

    # Search for contacts
    results = pb.search_contacts('John')
    for contact in results:
        pb.display_contact_info(contact)

    # Save the phonebook to a file
    pb.save_to_file('phonebook.json', 'json')

    # Load phonebook data from a file
    pb.load_from_file('phonebook.json', 'json')
"""

import json
import yaml
from typing import List
from lib.person import Person
from config.baseconfig import styling as style



class Phonebook:
    """
    A class that represents a phonebook, containing a list of Person objects
    """

    def __init__(self):
        """
        Initialize an empty phonebook
        """
        self.contacts = []

    def add_contact(self, person: Person):
        """
        Add a new contact to the phonebook

        Args:
            person (Person): a Person object representing the contact to add
        """
        self.contacts.append(person)

    def remove_contact(self, person: Person):
        """
        Remove a contact from the phonebook

        Args:
            person (Person): a Person object representing the contact to remove
        """
        self.contacts.remove(person)

    def update_contact(self, person: Person):
        """
        Update a contact in the phonebook.

        Args:
            person (Person): The updated Person object representing the contact.
        """
        for index, contact in enumerate(self.contacts):
            if contact.full_name == person.full_name:
                self.contacts[index] = person
                break
        else:
            raise ValueError("Contact not found in the phonebook.")
        
    def get_contacts(self) -> List[Person]:
        """
        Get all contacts in the phonebook

        Returns:
            List[Person]: a list of all Person objects in the phonebook
        """
        return self.contacts

    def save_to_file(self, filename: str, file_format: str):
        """
        Serialize the phonebook data to a file in the specified format

        Args:
            filename (str): the name of the file to save the data to
            format (str): the format to use for serialization ('json' or 'yaml')
        """
        data = {contact.full_name: contact.__dict__ for contact in self.contacts}

        with open(filename, 'w') as data_file:
            if file_format == 'json':
                json.dump(data, data_file, indent=4)
            elif file_format == 'yaml':
                #yaml.add_representer(Person, self.person_representer)
                yaml.dump(data, data_file)

    def load_from_file(self, filename: str, file_format: str):
        """
        Load phonebook data from a file in the specified format

        Args:
            filename (str): the name of the file to load the data from
            format (str): the format to use for deserialization ('json' or 'yaml')
        """
        with open(filename, 'r') as data_file:
            if file_format == 'json':
                data = json.load(data_file)
            
            elif file_format == 'yaml':
                data = yaml.safe_load(data_file)

            for contact_info in data.values():
                contact = Person.from_dict(contact_info)
                self.contacts.append(contact)                

    def search_contacts(self, query: str) -> List[Person]:
        """
        Search for contacts in the phonebook based on the given query.

        Args:
            query (str): The search query, which can be a first name, last name,
                         full name, phone, or address.

        Returns:
            List[Person]: A list of Person objects matching the search query.
        """
        results = []
        query = query.lower()
        
        for contact in self.contacts:
            if ((contact.first_name and query in contact.first_name.lower()) or
                    (contact.last_name and query in contact.last_name.lower()) or
                    (contact.full_name and query in contact.full_name.lower()) or
                    (contact.phone and query in contact.phone.lower()) or
                    (contact.address and query in contact.address.lower())):
                
                results.append(contact)
        
        return results
    
    def display_contact_info(self, person, item_number=None):
        """
        Prints the given contact's data on the screen.

        Args:
            person (Person): A single contact object.
            item_number (int, optional): The number of the contact to be printed, if desired.
                                         This has been specified for interaction purposes if needed.
        """

        print('\n')
        if item_number is not None:
            print('{}Item number: {}{}'.format(style["GREEN"], item_number, style["END"]))

        for item, value in person.__dict__.items():
            print('  {: >15} : {}'.format(item.replace('_', ' '), value))

    def display_all_contacts(self):
        """
        Display information for all contacts in the phonebook.

        Args:
            phonebook (Phonebook): The Phonebook instance containing the contacts.

        Returns:
            None
        """
        for contact in self.contacts:
            self.display_contact_info(contact)
