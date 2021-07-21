from __future__ import print_function, unicode_literals
from PyInquirer import prompt
from examples import custom_style_2
import requests
import json
from sourdough.communication.messages import SuccessMessage, deserialize_message

# TODO:
# 1.An action selector function(the user selects an action)
# 2.An entry for the SourdoughPy, confirm account or sign up function, will call action selector function.
# 3.A while loop to go over each action and select the function to get the info for that action.
# 4.At the end of the action with the success message, ask if the user wants to do another action or exit.


def get_account_info():
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


def get_water_and_flour_weights():
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


def get_target_info():
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


def get_extraction_info():
    question = [
        {
            'type': 'input',
            'name': 'sourdough_weight_used_in_grams',
            'message': 'How many sourdough starter did you extract?, in grams'
        }
    ]
    answer = prompt(question, style=custom_style_2)
    return answer['sourdough_weight_used_in_grams']


def get_refrigeration_action():
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


if __name__ == '__main__':
    name, last_name, email = get_account_info()
    #water, flour = get_water_and_flour_weights()
    r = requests.post(
        "http://127.0.0.1:5000/create_account",
        params={"name": name, "last_name": last_name, "email": email}
    )
    response = json.loads(r.text)
    print(response)
    message = deserialize_message(response)
    print(message)
