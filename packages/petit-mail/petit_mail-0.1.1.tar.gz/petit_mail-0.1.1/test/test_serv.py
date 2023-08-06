import requests
import sys

url = 'http://localhost:5004'


def test(account:str ):

    data = {
        'subject': 'Flask',
        'content': '<p><strong>Sent from flask</strong></p>',
        'addresses': ['pleveau@juniorisep.com'],
        'data': {
            "front_url": "https://phoenix.juniorisep.com",
            "mission": {
                "id": 4544,
                "name": "test",
                "projectManager": {
                    "student": {
                        'lastName': 'Leveau',
                        'firstName': 'Paul'
                    }
                }
            },
            "validationType": {
                "value": "Technique",
            },
            "validator": {
                "student": {
                    "firstName": "Paull",
                    "lastName": "Leveau"
                }
            },
            "document": {
                "type": {
                    "value": "DDE"
                },
                "reference": "DDE-XXX"
            }
        },
        'from': 'pegasus',
        'template_name': 'validation/request_validation',
    }


    res = requests.post(url+f'/send_mail/{account}/html', json=data)

    print(res)


if __name__ == '__main__':
    test(sys.argv[1])
