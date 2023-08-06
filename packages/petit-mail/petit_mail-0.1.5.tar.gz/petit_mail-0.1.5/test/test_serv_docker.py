import requests

url = 'http://localhost:5004'


def _reload():
    requests.get(url+'/reload')


send = True


def test():

    data = {
        'addresses': ['pleveau@juniorisep.com'],
        'data': {
            'mission_name': 'test',
            'docker_name': 'docker_wp',
            'virtual_host': "etudes.docker.juniorisep.com",
            'port': 40031,
            'password': 'debNation',
            'operation_date': 'Today',
            "custom": """
            test
            """
        },
        'from': 'JuniorISEP | Docker',
        'template_name': 'example/docker',
    }

    res = requests.post(
        url+f'/send_mail/info/html?send={int(send)}', json=data)

    with open('test.html', 'w') as f:
        f.write(res.text)


if __name__ == '__main__':
    _reload()
    test()
