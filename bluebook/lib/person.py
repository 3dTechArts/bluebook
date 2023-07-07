"""
This module defines a Person class with name, phone number, and address attributes.
The class allows setting and getting the phone number and address using properties.
It also provides a string representation of the person object.

Module: person.py
Author: [Author Name]

Classes:
    Person: Represents a person with first name, last name, phone number, and address.

Usage:
    # Create a Person object
    person = Person('John', 'Doe')

    # Set phone number and address
    person.phone = '1234567890'
    person.address = '123 Main Street'

    # Get phone number and address
    phone_number = person.phone
    address = person.address

    # String representation of the person object
    print(person)

"""

class Person:
    """
    This class inherits from the object class and represents a Person object
    with first and last names, phone number, and address attributes.
    """

    def __init__(self, first_name: str, last_name: str, phone=None, address=None):
        """
        Initialize a new Person object.

        Args:
            first_name (str): The first name of the person.
            last_name (str): The last name of the person.
            phone (str, optional): The phone number of the person. Defaults to None.
            address (str, optional): The address of the person. Defaults to None.
        """

        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.address = address
        self.full_name = '{} {}'.format(self.first_name, self.last_name)
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a new Person object from a dictionary.

        Args:
            data (dict): A dictionary containing the person's information.

        Returns:
            Person: A new Person object.
        """
        return cls(
            data["first_name"],
            data["last_name"],
            phone=data.get("phone"),
            address=data.get("address"),
        )
