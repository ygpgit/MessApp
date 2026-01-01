import os
import json
import re
import subprocess
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# File to store contacts and groups
DATA_FILE = "contacts.json"

def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def load_data():
    """Load contacts and groups from JSON file. If file does not exist, return an empty dictionary."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(Fore.RED + "⚠️ Error: Invalid JSON format. Resetting...")
            return {"contacts": {}, "groups": {}}
    return {"contacts": {}, "groups": {}}

def save_data(data):
    """Save contacts and groups to JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(Fore.RED + f"⚠️ Error saving data: {e}")

def is_valid_phone_number(phone_number):
    """Validate that the phone number is exactly 10 digits."""
    return re.fullmatch(r"\d{10}", phone_number) is not None

def create_contact():
    """Create a new contact."""
    clear_screen()
    print(Fore.BLUE + "\t=== Create Contact ===")
    data = load_data()

    contact_name = input(Fore.YELLOW + "Enter contact name: ").strip()
    phone_number = input(Fore.CYAN + "Enter phone number: ").strip()

    if not contact_name or not phone_number:
        print(Fore.RED + "⚠️ Error: Name and number cannot be empty!")
        return

    if is_valid_phone_number(phone_number):
        data["contacts"][contact_name] = phone_number
        save_data(data)
        print(Fore.GREEN + f"✅ Contact '{contact_name}' added successfully!")
    else:
        print(Fore.RED + "⚠️ Invalid phone number. Please enter a valid 10-digit number.")

def create_edit_group():
    """Create or edit a contact group."""
    clear_screen()
    print(Fore.BLUE + "\t=== Create/Edit Group ===")
    data = load_data()

    group_name = input(Fore.YELLOW + "Enter group name: ").strip()
    if not group_name:
        print(Fore.RED + "⚠️ Group name cannot be empty!")
        return

    if group_name not in data["groups"]:
        data["groups"][group_name] = []

    while True:
        clear_screen()
        print(Fore.BLUE + f"\t=== Editing Group: {group_name} ===")
        print(Fore.GREEN + "Current Members:")
        for member in data["groups"][group_name]:
            print(f"- {member} ({data['contacts'].get(member, 'Unknown')})")

        print(Fore.CYAN + "\nOptions:")
        print("1. Add Member")
        print("2. Remove Member")
        print("3. Save and Exit")

        choice = input(Fore.MAGENTA + "Enter your choice: ").strip()
        
        if choice == "1":
            contact_name = input(Fore.YELLOW + "Enter contact name: ").strip()
            if contact_name in data["contacts"]:
                data["groups"][group_name].append(contact_name)
                print(Fore.GREEN + "✅ Contact added successfully!")
            else:
                print(Fore.RED + "⚠️ Contact does not exist. Please add it first.")

        elif choice == "2":
            member_to_remove = input(Fore.YELLOW + "Enter contact name to remove: ").strip()
            if member_to_remove in data["groups"][group_name]:
                data["groups"][group_name].remove(member_to_remove)
                print(Fore.GREEN + "✅ Member removed successfully!")
            else:
                print(Fore.RED + "⚠️ Member not found in this group.")

        elif choice == "3":
            save_data(data)
            print(Fore.GREEN + f"✅ Group '{group_name}' updated successfully!")
            break
        else:
            print(Fore.RED + "⚠️ Invalid choice. Please try again.")

def send_message():
    """Send a message to an individual contact or group."""
    data = load_data()
    
    recipient = input(Fore.YELLOW + "Enter name or group to send message: ").strip()
    
    if recipient in data["contacts"]:
        phone_or_email = data["contacts"][recipient]
        message = input(Fore.CYAN + "Type your message: ").strip()
        send_via_messages(phone_or_email, message)

    elif recipient in data["groups"]:
        message = input(Fore.CYAN + "Type your message: ").strip()
        for member in data["groups"][recipient]:
            first_name = member.split()[0]
            personalized_message = f"{first_name}, {message}"
            phone_or_email = data["contacts"][member]
            send_via_messages(phone_or_email, personalized_message)
    else:
        print(Fore.RED + "⚠️ Contact or group not found!")

def send_via_messages(phone_or_email, message):
    """Use AppleScript to send a message via the Mac Messages app."""
    applescript = f'''
    tell application "Messages"
        set targetBuddy to "{phone_or_email}"
        set targetService to 1st service whose service type is iMessage
        set chat to make new chat with properties {{service:targetService, participants:targetBuddy}}
        send "{message}" to chat
    end tell
    '''
    subprocess.run(["osascript", "-e", applescript])
    print(f"✅ Sent message to {phone_or_email}: {message}")

def main_menu():
    """Main menu of the message app."""
    while True:
        clear_screen()
        print(Fore.MAGENTA + "\t=== Message Scheduler ===")
        print(Fore.CYAN + "1. Create Contact")
        print(Fore.CYAN + "2. Create/Edit Group")
        print(Fore.CYAN + "3. Send Message")
        print(Fore.CYAN + "4. Exit")
        
        choice = input(Fore.YELLOW + "Enter your choice: ").strip()
        
        if choice == "1":
            create_contact()
        elif choice == "2":
            create_edit_group()
        elif choice == "3":
            send_message()
        elif choice == "4":
            print(Fore.GREEN + "🚀 Exiting... Goodbye!")
            break
        else:
            print(Fore.RED + "⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    print(Fore.BLUE + "Loading contacts and groups...")
    data = load_data()
    print(Fore.GREEN + "✅ Data loaded successfully!")
    main_menu()

