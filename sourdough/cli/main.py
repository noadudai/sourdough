from __future__ import print_function, unicode_literals

from typing import List

import requests
import json

from sourdough.cli.prompts import ask_for_action_prompt, get_account_info_prompt, get_email_prompt, \
    get_feeding_action_info_prompt, get_target_info_prompt, get_extraction_info_prompt, get_refrigeration_action_prompt, \
    stay_or_leave_prompt, has_account_prompt
from sourdough.communication.actions import FeedingAction, ExtractionAction, RefrigerationAction
from sourdough.communication.messages import SuccessMessage, deserialize_message, PerformActionsMessage, Message, \
    FailedMessage

BREAD_ASCII_ART = """      
                             ██████████████                          
                     ████████▓▓▓▓██░░░░██▓▓████                      
             ████████░░░░░░░░██▓▓██░░░░██▓▓▓▓▓▓██                    
         ████░░██▓▓▓▓██░░░░░░██▓▓▓▓██░░██▓▓▓▓▓▓▓▓██                  
     ████░░░░░░░░██▓▓▓▓██░░░░██▓▓▓▓██░░██▓▓▓▓▓▓▓▓██                  
   ██▓▓▓▓██░░░░░░░░██▓▓▓▓██░░██▓▓▓▓██░░██▓▓▓▓▓▓██                    
 ██▓▓▓▓▓▓▓▓██░░░░░░██▓▓▓▓██░░██▓▓▓▓██░░██▓▓▓▓▓▓██                    
 ██▓▓▓▓▓▓▓▓▓▓██░░░░██▓▓▓▓██░░██▓▓▓▓▓▓██▓▓▓▓▓▓▓▓██                    
 ██▓▓▓▓▓▓▓▓▓▓▓▓██░░██▓▓▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██                      
 ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████                        
 ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████                            
   ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████                                
       ████████▓▓▓▓▓▓▓▓▓▓▓▓██████                                    
               ████████████                                          
"""


def deserialize_response(response, expected_message_types=None) -> Message:
    serialized_response = json.loads(response)
    message = deserialize_message(serialized_response)
    if expected_message_types:
        for message_type in expected_message_types:
            if isinstance(message, message_type):
                return message
        # If non of the type checks worked its not of the right type
        raise Exception(
            f"Message serialized but was not of the expected type {expected_message_types} -> {type(message)}")
    return message


def create_account():
    name, last_name, email = get_account_info_prompt()
    request = requests.post(
        "http://127.0.0.1:5000/create_account",
        params={"name": name, "last_name": last_name, "email": email}
    )
    message = deserialize_response(request.text, expected_message_types=[SuccessMessage, FailedMessage])

    if isinstance(message, SuccessMessage):
        return email

    if isinstance(message, FailedMessage):
        raise Exception(f"Failed to sign up {message}")


def login():
    email = get_email_prompt()
    request = requests.post(
        "http://127.0.0.1:5000/is_user_in_database",
        params={"email": email}
    )
    response = json.loads(request.text)
    message = deserialize_message(response)
    if isinstance(message, SuccessMessage):
        return email
    else:
        print(message)
        raise Exception("Failed to login in")


def do_a_feeding_action(user_email):
    water, flour = get_feeding_action_info_prompt()
    request = requests.post(
        "http://127.0.0.1:5000/add_a_feeding_action",
        params={'email': user_email, 'water_weight_added_in_grams': water, 'flour_weight_added_in_grams': flour}
    )
    response = json.loads(request.text)
    message = deserialize_message(response)
    print(message)


def do_an_extraction_action(user_email):
    sourdough_weight = get_extraction_info_prompt()
    request = requests.post(
        "http://127.0.0.1:5000/add_extraction",
        params={"email": user_email, "sourdough_weight_used_in_grams": sourdough_weight}
    )
    response = json.loads(request.text)
    message = deserialize_message(response)
    print(message)


def do_a_refrigeration_action(user_email):
    in_or_out = get_refrigeration_action_prompt()
    request = requests.post(
        "http://127.0.0.1:5000/add_a_refrigerator_action",
        params={'email': user_email, 'in_or_out': in_or_out}
    )
    response = json.loads(request.text)
    message = deserialize_message(response)
    print(message)


def do_a_target_action(user_email):
    date_of_action, weight = get_target_info_prompt()
    request = requests.post(
        "http://127.0.0.1:5000/add_a_target",
        params={'email': user_email, 'date_of_action': date_of_action, 'sourdough_weight_target_in_grams': weight}
    )
    response = json.loads(request.text)
    message = deserialize_message(response)
    print(message)


def do_actions_today(user_email):
    request = requests.post(
        "http://127.0.0.1:5000/my_action_today",
        params={'email': user_email}
    )

    message = deserialize_response(request.text, expected_message_types=[PerformActionsMessage, FailedMessage])

    if isinstance(message, PerformActionsMessage):
        for action in message.actions:
            if isinstance(action, FeedingAction):
                print(
                    f"Please feed your sourdough starter with {action.water}grams water, and {action.flour}grams flour"
                )
            elif isinstance(action, ExtractionAction):
                print(f"Please extract {action.extraction_weight}")
            elif isinstance(action, RefrigerationAction):
                if action.in_or_out == 'in':
                    print("Please put your sourdough in the refrigerator")
                else:
                    print("Please take your sourdough stater out of the refrigerator")

    if isinstance(message, FailedMessage):
        raise Exception(f"Actions today failed unexpectedly {message}")


def sign_up_or_login() -> str:
    if has_account_prompt():
        return login()
    else:
        return create_account()


def select_and_perform_action(email):
    action = ask_for_action_prompt()
    if action == 'feeding action':
        do_a_feeding_action(email)
    elif action == 'extraction action':
        do_an_extraction_action(email)
    elif action == 'refrigeration action':
        do_a_refrigeration_action(email)
    elif action == 'target action':
        do_a_target_action(email)
    elif action == 'what do i need to do today?':
        do_actions_today(email)
    else:
        raise Exception("Unknown action input")

def start():
    print("Welcome to SourdoughPy")
    print(BREAD_ASCII_ART)
    email = sign_up_or_login()
    select_and_perform_action(email)
    while stay_or_leave_prompt():
        select_and_perform_action(email)
    else:
        print("Thank you!, see you tomorrow.")


if __name__ == '__main__':
    start()
