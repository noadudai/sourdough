import requests
from PyInquirer import prompt, print_json


def get_email_address():
    questions = [
        {
            'type': 'input',
            'name': 'email_address',
            'message': 'What\'s your email address',
        }
    ]

    answers = prompt(questions)
    return answers["email_address"]


if __name__ == '__main__':
    email = get_email_address()
    r = requests.post(
        "http://127.0.0.1:5000/create_account",
        json={"name": "noa", "last_name": "dudai", "email": email}
    )
