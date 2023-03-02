from base64 import b64encode
from pathlib import Path
from re import search
from requests import request
from subprocess import getoutput
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning


class Client:
    _headers = None
    _port = None

    @staticmethod
    def call(method, endpoint, json=None):
        url = f'https://127.0.0.1:{Client._port}{endpoint}'
        return request(method, url, headers=Client._headers, json=json, verify=False)

    @staticmethod
    def connect():
        install_directory = Client._get_install_directory()
        port, password = Client._get_lockfile_data(install_directory)
        Client._port = port
        Client._headers = {'Authorization': f'Basic {Client._get_auth(password)}'}

    @staticmethod
    def _get_install_directory():
        client_process_args = getoutput('wmic PROCESS WHERE name="LeagueClientUx.exe" GET commandline')
        install_directory = search('--install-directory=[^"]*', client_process_args)
        if install_directory:
            return Path(install_directory.group()[20:])
        else:
            return Path.home() / 'Riot Games' / 'League of Legends'

    @staticmethod
    def _get_lockfile_data(path):
        lockfile = open(path / 'lockfile')
        data = lockfile.read().split(':')
        lockfile.close()
        return [data[2], data[3]]

    @staticmethod
    def _get_auth(password):
        return b64encode(bytes(f'riot:{password}', 'utf-8')).decode('ascii')


class Store:
    _headers = None
    _server = None

    @staticmethod
    def call(method, endpoint, json=None):
        url = f'https://{Store._server}.store.leagueoflegends.com/storefront/v3{endpoint}'
        return request(method, url, headers=Store._headers, json=json, verify=False)

    @staticmethod
    def connect():
        server = Store._get_server()
        id_token = Store._get_id_token()
        platforms = {
            'BR': 'br', 'EUNE': 'eun', 'EUW': 'euw', 'LAN': 'la1', 'LAS': 'la2', 'NA': 'na', 'OCE': 'oc', 'RU': 'ru',
            'TR': 'tr', 'JP': 'jp', 'KR': 'kr'
        }
        Store._server = platforms[server]
        Store._headers = {'Authorization': f'Bearer {id_token}'}

    @staticmethod
    def _get_server():
        return Client.call('GET', '/riotclient/get_region_locale').json()['region']

    @staticmethod
    def _get_id_token():
        return Client.call('GET', '/lol-login/v1/session').json()['idToken']


disable_warnings(InsecureRequestWarning)
Client.connect()
Store.connect()
