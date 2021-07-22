from PyInquirer import prompt
from examples import custom_style_2


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


def get_email_prompt():
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


def stay_or_leave_prompt():
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


def has_account_prompt() -> bool:
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