import requests
import os
from pprint import PrettyPrinter

pprinter = PrettyPrinter()

HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'
}


def link_download_runner(org, archi='x64'):
    download_link = f'https://api.github.com/orgs/{org}/actions/runners/downloads'
    return next(
        elem
        for elem in requests.get(download_link, headers=HEADERS).json()
        if elem['os'] == 'linux' and elem['architecture'] == archi
    )


def infos_runners(org):
    print(HEADERS)
    info_link = f'https://api.github.com/orgs/{org}/actions/runners'
    return requests.get(info_link, headers=HEADERS).json()


def list_runners(org):
    list_link = f'https://api.github.com/orgs/{org}/actions/runners'
    response = requests.get(list_link, headers=HEADERS)
    pprinter.pprint(response.json())
    return response.json()


def create_runner_token(org):
    """
    Create  a token used as paramert of the github action script start,
    this token is available one hour.
    `./config.sh --url URL --token TOKEN`
    :return:
    """
    token_link = f'https://api.github.com/orgs/{org}/actions/runners/registration-token'
    response = requests.post(token_link, headers=HEADERS).json()

    pprinter.pprint(response)
    return response['token']


def force_delete_runner(org, runner_id):
<<<<<<< HEAD
    runner_link = f'https://api.github.com/orgs/{org}/actions/runners/{runner_id}'
    response = requests.delete(runner_link, headers=HEADERS)
=======
    """
    :return:
    """
    response = requests.delete(f'https://api.github.com/orgs/{org}/actions/runners/{runner_id}', headers=HEADERS)
>>>>>>> 4fa77ef ([RELENG-4473] main-logic)
    if response.status_code != 204:
        raise Exception("Error in response")
