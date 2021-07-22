from __future__ import print_function, unicode_literals
from PyInquirer import prompt
from examples import custom_style_2
import requests
import json

from sourdough.communication.actions import deserialize_actions, FeedingAction, ExtractionAction, RefrigerationAction
from sourdough.communication.messages import SuccessMessage, deserialize_message, FailedMessage, PerformActionsMessage
import datetime

# 2.An entry for the SourdoughPy, confirm account or sign up function, will call action selector function.
# 3.A while loop to go over each action and select the function to get the info for that action.
# 4.At the end of the action with the success message, ask if the user wants to do another action or exit.
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


# 1
def ask_for_action_prompt():
    actions_prompt = {
        'type': 'list',
        'name': 'actions',
        'message': 'Which action would you like to perform?',
        'choices': [
            'what do i need to do today?',
            'target action',
            'feeding action',
            'extraction action',
            'refrigeration action'
        ]
    }
    answers = prompt(actions_prompt)
    return answers['actions']


def get_account_info_prompt():
    questions = [
        {
            'type': 'input',
            'name': 'name',
            'message': 'What is your name?'
        },
        {
            'type': 'input',
            'name': 'last_name',
            'message': 'What is your last name?'
        },
        {
            'type': 'input',
            'name': 'email',
            'message': 'What is your Email address?'
        }
    ]
    answers = prompt(questions, style=custom_style_2)
    return answers["name"], answers["last_name"], answers["email"]


def get_email():
    question = [
        {
            'type': 'input',
            'name': 'email',
            'message': 'Please enter your email address:'
        }
    ]
    answer = prompt(question, style=custom_style_2)
    return answer['email']


def get_feeding_action_info_prompt():
    questions = [
        {
            'type': 'input',
            'name': 'water_added_in_grams',
            'message': 'How much water did you use?, in grams'
        },
        {
            'type': 'input',
            'name': 'flour_added_in_grams',
            'message': 'How much flour did you use?, in grams'
        }
    ]
    answers = prompt(questions, style=custom_style_2)
    return answers["water_added_in_grams"], answers["flour_added_in_grams"]


def get_target_info_prompt():
    questions = [
        {
            'type': 'input',
            'name': 'date_of_action',
            'message': 'Please enter the targeted date:'
        },
        {
            'type': 'input',
            'name': 'sourdough_weight_target_in_grams',
            'message': "How much sourdough starter do you need for this target?, in grams"
        }
    ]
    answers = prompt(questions, style=custom_style_2)
    return answers['date_of_action'], answers['sourdough_weight_target_in_grams']


def get_extraction_info_prompt():
    question = [
        {
            'type': 'input',
            'name': 'sourdough_weight_used_in_grams',
            'message': 'How many sourdough starter did you extract?, in grams'
        }
    ]
    answer = prompt(question, style=custom_style_2)
    return answer['sourdough_weight_used_in_grams']


def get_refrigeration_action_prompt():
    question = [
        {
            'type': 'list',
            'name': 'in_or_out',
            'message': 'Did you put your sourdough starter in or did you take yit out of the refrigerator?',
            'choices': [
                'in',
                'out'
            ]
        }
    ]
    answer = prompt(question, style=custom_style_2)
    return answer['in_or_out']


def stay_or_leave():
    question = [
        {
            'type': 'list',
            'name': 'stay_or_leave',
            'message': 'Do you want to perform another action?',
            'choices': [
                'do another action',
                'logout'
            ]
        }
    ]
    answers = prompt(question, style=custom_style_2)
    return answers['stay_or_leave'] == "do another action"


def has_account() -> bool:
    question = [
        {
            'type': 'list',
            'name': 'existing_account',
            'message': 'login or sign up',
            'choices': [
                'login',
                'sign up'
            ]
        }
    ]
    answers = prompt(question, style=custom_style_2)
    return answers['existing_account'] == "login"


def create_account():
    name, last_name, email = get_account_info_prompt()
    request = requests.post(
        "http://127.0.0.1:5000/create_account",
        params={"name": name, "last_name": last_name, "email": email}
    )
    response = json.loads(request.text)
    message = deserialize_message(response)
    if isinstance(message, SuccessMessage):
        return email
    else:
        print(message)
        raise Exception("Failed to sign up")


def login():
    email = get_email()
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

    response = json.loads(request.text)
    message = deserialize_message(response)
    if isinstance(message, PerformActionsMessage):
        for action in message.actions:
            if isinstance(action, FeedingAction):
                print(
                    "Please feed your sourdough starter with " +
                    str(action.water) + "grams water, and " +
                    str(action.flour) + "grams flour"
                )
            elif isinstance(action, ExtractionAction):
                print(
                    "Please extract " +
                    str(action.extraction_weight) +
                    "grams from your sourdough starter"
                )
            elif isinstance(action, RefrigerationAction):
                if action.in_or_out == 'in':
                    print(
                        "Please put your sourdough in the refrigerator"
                    )
                else:
                    print(
                        "Please take your sourdough stater out of the refrigerator"
                    )
    else:
        print(message)
        raise Exception("Actions today returned unexpected message type")


def sign_up_or_login() -> str:
    if has_account():
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


def start():
    print("Welcome to SourdoughPy.")
    print(BREAD_ASCII_ART)
    email = sign_up_or_login()
    select_and_perform_action(email)
    while stay_or_leave():
        select_and_perform_action(email)
    else:
        print("Thank you!, see you tomorrow.")


if __name__ == '__main__':
    start()

