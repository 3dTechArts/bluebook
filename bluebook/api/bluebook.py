#!/usr/bin/env python3
"""
This module implements an API for managing a phonebook. It provides functionality to add,
remove, update, search, and export contacts in the phonebook.

Usage examples:

To search for contacts by name:
phonebook.py -s John Doe
To add a new contact:
phonebook.py -a
To remove an existing contact:
phonebook.py -r John Doe
To update an existing contact:
phonebook.py -u John Doe
To export the phonebook in JSON format:
phonebook.py --export_json
To export the phonebook in YAML format:
phonebook.py --export_yaml


Module Structure:
- Import required modules and dependencies.

- Define functions:
    get_target_contact(name_info, phonebook): Finds and returns a contact from the phonebook
        based on the provided name information.

    add_contact(args, phonebook): Handles the 'add' command to add a new contact to the phonebook.

    remove_contact(args, phonebook): Handles the 'remove' command to remove an existing
        contact from the phonebook.

    update_contact(args, phonebook): Handles the 'update' command to update an existing
        contact in the phonebook.

    search_contacts(args, phonebook): Handles the 'search' command to search for contacts
        by name in the phonebook.

    export_phonebook(phonebook, export_format): Exports the phonebook instance to a JSON or YAML
        file.

    handle_commands(args, phonebook): Handles the specified command based on the provided arguments.

    get_options(): Defines the command-line arguments and options.

    main(): Entry point of the API. Parses command-line arguments, creates a Phonebook instance,
        and executes the requested command.

"""


import os
import argparse
from datetime import datetime
import webbrowser

from lib.person import Person
from lib.phonebook import Phonebook
from config.baseconfig import JSON_DATABASE_FILE
from config.baseconfig import EXPORTS_DIR
from config.baseconfig import styling as style




def get_target_contact(name_info, phonebook):
    """
    Finds and returns a contact from the phonebook based on the provided name information.

    This function searches for contacts in the phonebook using the provided name information and
    interactively selects the contact to be returned.

    Args:
        name_info (list): A list of name components to search for in the phonebook.
        phonebook (Phonebook): An instance of the Phonebook class containing the contacts.

    Returns:
        Contact: The selected contact object if confirmed for removal, or None if canceled.

    """
    # Join the name components into a single string
    name = ' '.join(name_info)

    # Search for contacts in the phonebook based on the provided name
    contacts = phonebook.search_contacts(name)

    if not contacts:
        print("No contacts found with the provided name.")
        return None

    if len(contacts) == 1:
        # Only one contact found, display its information
        contact = contacts[0]
        phonebook.display_contact_info(contact)
    else:
        print("Multiple contacts found with the provided name. "
              "Please choose one of the followings:")
        
        for i, contact in enumerate(contacts, start=1):
            # Display information for each contact along with item numbers
            phonebook.display_contact_info(contact, item_number=i)
        while True:
            choice = input(f"\n{style['CYAN']}Which item number would you like "
                           f"to proceed with: {style['END']}")
            try:
                choice = int(choice)
                if 1 <= choice <= len(contacts):
                    break
            except ValueError:
                pass
            print("Invalid choice. Please try again.")

        # Get the selected contact based on the user's choice
        contact = contacts[choice - 1]

    # Ask for confirmation
    confirmation = input(f"\n{style['ORANGE']}Are you sure you want to proceed with "
                         f"this contact? (yes/no):{style['END']} ")

    while confirmation.lower() not in ['yes', 'y', 'no', 'n']:
        print(f"{style['PURPLE']}Not a valid entry!{style['END']}")
        confirmation = input(f"\n{style['ORANGE']}Are you sure you want to proceed "
                             f"with this contact? (yes/no):{style['END']} ")

    if confirmation.lower() not in ['yes', 'y']:
        print("Canceled.")
        return None

    return contact



def add_contact(args, phonebook):
    """
    Handle the 'add' command.

    This function adds a new contact to the phonebook based on the provided arguments.

    Args:
        args (argparse.Namespace): The parsed command-line arguments containing the
        contact information to add.
        phonebook (Phonebook): The Phonebook instance to add the contact to.

    Returns:
        None
    """
    while True:
        # Prompt for missing first name and last name if not provided through command-line arguments
        if not args.first_name and not args.last_name:
            if not args.first_name:
                args.first_name = input(f"{style['CYAN']}Enter the First name: {style['END']}")
            if not args.last_name:
                args.last_name = input(f"{style['CYAN']}Enter the Last name: {style['END']}")
        
        # Prompt for missing phone number and address if not provided through command-line arguments
        if not args.phone and not args.address:
            if not args.phone:
                args.phone = input(f"{style['CYAN']}Enter the Phone number: {style['END']}")
            if not args.address:
                args.address = input(f"{style['CYAN']}Enter the Address: {style['END']}")

        # Check if any of the required fields are empty
        if (args.first_name or args.last_name) and (args.phone or args.address):
            break

        print(f"{style['ORANGE']}Either a First or Last name along with at least a phone number or an address "
              "is required. Please try again!{style['END']}")

    # Create a new Person object with the provided information
    person = Person(args.first_name or "", 
                    args.last_name or "", 
                    args.phone or "", 
                    args.address or "")

    # Add the new contact to the phonebook
    phonebook.add_contact(person)

    print("Contact added successfully!")


def remove_contact(args, phonebook):
    """
    Handle the 'remove' command.

    This function removes a contact from the phonebook based on the provided arguments.

    Args:
        args (argparse.Namespace): The parsed command-line arguments containing the contact
        information to remove.
        phonebook (Phonebook): The Phonebook instance to remove the contact from.

    Returns:
        None
    """
    # Search for the contact to remove based on the given command-line arguments
    contact = get_target_contact(args.remove, phonebook)
    if not contact:
        return
    
    # Remove the contact from the phonebook
    phonebook.remove_contact(contact)
    print("Contact removed successfully!")



def update_contact(args, phonebook):
    """
    Handle the 'update' command.

    This function updates a contact in the phonebook with the provided information.

    Args:
        args (argparse.Namespace): The parsed command-line arguments containing the updated
        contact information.
        phonebook (Phonebook): The Phonebook instance to update.

    Returns:
        None
    """
    # Search for the contact to update based on the given command-line arguments
    contact = get_target_contact(args.update, phonebook)
    if not contact:
        return

    # Prompt for missing information if not provided through command-line arguments
    if not args.first_name and not args.last_name:
        while not args.first_name and not args.last_name:
            print(f"\n{style['GREEN1']}At least one of First or Last name is "
                  f"required!{style['END']}")
            
            args.first_name = input(f"{style['YELLOW']}Enter the updated "
                                    f"First name: {style['END']}")
            args.last_name = input(f"{style['YELLOW']}Enter the updated "
                                   f"Last name: {style['END']}")

    if not args.phone and not args.address:
        while not args.phone and not args.address:
            print(f"\n{style['PURPLE']}At least one of Phone or Address is "
                  f"required! {style['END']}")
            
            args.phone = input(f"{style['CYAN']}Enter the updated phone number: {style['END']}")
            args.address = input(f"{style['CYAN']}Enter the updated address: {style['END']}")

    # Update the selected contact with the provided information
    contact.first_name = args.first_name or ""
    contact.last_name = args.last_name or ""
    contact.phone = args.phone or ""
    contact.address = args.address or ""

    # Update the contact in the phonebook
    phonebook.update_contact(contact)
    print("Contact updated successfully!")


def search_contacts(args, phonebook):
    """
    Handle the 'search' command.

    This function searches for contacts in the phonebook that match the provided name 
    and displays the matching contacts.
    It returns a list of Contact objects representing the matching contacts.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        phonebook (Phonebook): The Phonebook instance.

    Returns:
        list: A list of Contact objects representing the matching contacts.
    """
    name = ' '.join(args.search)
    # Search for contacts matching the provided name
    search_results = phonebook.search_contacts(name)

    # Display the search results
    if search_results:
        print("Matching contacts:")
        for contact in search_results:
            phonebook.display_contact_info(contact)
        print('\n')
    else:
        print("No matching contacts found.")

    return search_results


def export_phonebook(phonebook, export_format):
    """
    Export the phonebook instance to a JSON or YAML file.

    This function exports the given Phonebook instance to a specified file format (JSON or YAML).
    The exported file is saved in the export directory (`EXPORTS_DIR`) with a filename based on 
    the current date and time.

    Args:
        phonebook (Phonebook): The Phonebook instance to be exported.
        export_format (str): The desired export format: 'json' or 'yaml'.

    Returns:
        (str): exported path string
    """

    # Create the export directory if it doesn't exist
    os.makedirs(EXPORTS_DIR, exist_ok=True)

    # Construct the export file path based on the current date and time
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    export_filename = f'phonebook-export-{timestamp}.{export_format}'
    export_path = os.path.join(EXPORTS_DIR, export_filename)

    # Export the phonebook to the JSON file
    phonebook.save_to_file(filename=export_path, file_format=export_format)

    print(f"Phonebook exported to: {export_path}")

    return export_path

def print_all_contacts(phonebook):
    """
    Prints the information for all contacts in the phonebook on the sceen

    Args:
        phonebook (Phonebook): The Phonebook instance containing the contacts.

    Returns:
        None
    """
    phonebook.display_all_contacts()

def generate_contacts_html(phonebook):
    """
    Generate an HTML representation of all contacts' information in the phonebook.

    Args:
        phonebook (Phonebook): The Phonebook instance containing the contacts.

    Returns:
        str: HTML representation of all contacts' information.
    """
    html = "<html>\n<head>\n<title>Contact Information</title>\n</head>\n<body>\n"
    
    for contact in phonebook.contacts:
        html += "<div>\n"
        html += f"<h2>{contact.full_name}</h2>\n"
        html += f"<p>First Name: {contact.first_name}</p>\n"
        html += f"<p>Last Name: {contact.last_name}</p>\n"
        html += f"<p>Phone: {contact.phone}</p>\n"
        html += f"<p>Address: {contact.address}</p>\n"
        html += "</div>\n"
    
    html += "</body>\n</html>"
    return html


def export_and_open_html(html_content):

    """
    Save HTML content to a file and open it in the system's default web browser.

    Args:
        html_content (str): The HTML content to be saved.
        filename (str): The name of the file to save the HTML content to.

    Returns:
        None
    """
    # construct the filename
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    export_path = os.path.join(EXPORTS_DIR, f'phonebook_html_{timestamp}.html')
    # Save the HTML content to a file
    with open(export_path, 'w') as html_file:
        html_file.write(html_content)

    # Open the HTML file in the system's default web browser
    webbrowser.open(export_path)
    print(f"Phonebook exported to: {export_path}")


def handle_commands(args, phonebook):
    # Handle the specified command based on the args provided
    if args.add:
        add_contact(args, phonebook)
    elif args.remove:
        remove_contact(args, phonebook)
    elif args.update:
        update_contact(args, phonebook)
    elif args.search:
        search_contacts(args, phonebook)
    elif args.export_json:
        export_phonebook(phonebook, 'json')
    elif args.export_yaml:
        export_phonebook(phonebook, 'yaml')
    elif args.display_all_contacts:
        print_all_contacts(phonebook)
    elif args.export_html:
        html = generate_contacts_html(phonebook)
        export_and_open_html(html)
    else:
        print("No valid command specified.")


def get_options():
    """
    Define the command-line arguments and options using argparse.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    # Define the usage examples for the epilog
    epilog = f"""
    
    Usage examples:
        1. Search for contacts by name:
            phonebook.py -s John Doe
            
        2. Add a new contact:
            phonebook.py -a --first-name John --last-name Doe --phone 123456 --address "123 Main St"
            
        3. Remove an existing contact:
            phonebook.py -r John Doe
    
        4. Update an existing contact:
            phonebook.py -u John Doe --phone 9876543210
            
        5. Export the phonebook in JSON format:
            phonebook.py --export_json
            
        6. Export the phonebook in YAML format:
            phonebook.py --export_yaml

    {style['CYAN']}upported formats:{style['END']} JSON/YAML/HTML
        """


    # Create an ArgumentParser instance with a description and usage
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Phonebook API: a tool for creating and managing '
                                                 'a phonebook.',
                                     usage='phonebook.py [options] ...',
                                     epilog=epilog)

    # Add arguments for the contact details
    parser.add_argument('-f', '--first-name', action='store', help='First name of the contact')
    parser.add_argument('-l', '--last-name', action='store', help='Last name of the contact')
    parser.add_argument('-p', '--phone', action='store', help='Phone number of the contact')
    parser.add_argument('-ad', '--address', action='store', help='Address of the contact')

    # Add mutually exclusive arguments for different actions
    action_grp = parser.add_mutually_exclusive_group(required=True)
    action_grp.add_argument('-s', '--search', action='store', nargs='+',
                            help='Search for contacts by name', required=False)
    action_grp.add_argument('-a', '--add', action='store_true',
                            help='Add a new contact', required=False)
    action_grp.add_argument('-r', '--remove', action='store', nargs='+',
                            help='Remove an existing contact', required=False)
    action_grp.add_argument('-u', '--update', action='store', nargs='+',
                            help='Update an existing contact', required=False)
    action_grp.add_argument('-d', '--display_all_contacts', action='store_true',
                            help='Prints out all the contacts in the phonebook on the screen',
                            required=False)

        
    # Add arguments for exporting the phonebook
    action_grp.add_argument('--export_json', action='store_true',
                            help='Export the phonebook in JSON format')
    action_grp.add_argument('--export_yaml', action='store_true',
                            help='Export the phonebook in YAML format')
    action_grp.add_argument('--export_html', action='store_true',
                            help='Export the phonebook in HTML format',
                            required=False)
    
    # Parse the command-line arguments
    args = parser.parse_args()

    return args











def main():
    """
    Entry point of the API. Parses command-line arguments, creates a Phonebook instance,
    and executes the requested command.

    Returns:
        None
    """
    args = get_options()

    # Creates a Phonebook instance and load the phonebook database from the file
    phonebook = Phonebook()
    phonebook.load_from_file(JSON_DATABASE_FILE, 'json')

    # Handle the specified command
    handle_commands(args, phonebook)

    # Save the phonebook to the database
    phonebook.save_to_file(JSON_DATABASE_FILE, file_format='json')




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt!')
        import sys
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
