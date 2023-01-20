from base64 import b64encode
from pathlib import Path
from re import search
from requests import request
from subprocess import getoutput
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning


disable_warnings(InsecureRequestWarning)


class Client:
    def __init__(self):
        self._headers = None
        self._port = None
        self.connect()

    def connect(self):
        install_directory = self._get_install_directory()
        port, password = self._get_lockfile_data(install_directory)
        self._port = port
        self._headers = {'Authorization': f'Basic {self._get_auth(password)}'}

    def call(self, method, endpoint, json=None):
        url = f'https://127.0.0.1:{self._port}{endpoint}'
        return request(method, url, headers=self._headers, json=json, verify=False)

    @staticmethod
    def _get_install_directory():
        client_process_args = getoutput('wmic PROCESS WHERE name="LeagueClientUx.exe" GET commandline')
        install_directory = search('--install-directory=[^"]*', client_process_args)
        if install_directory:
            return install_directory.group()[20:]
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
    def __init__(self):
        self._headers = None
        self._server = None
        self.connect()

    def connect(self):
        client = Client()
        server = self._get_server(client)
        id_token = self._get_id_token(client)
        platforms = {
            'BR': 'br', 'EUNE': 'eun', 'EUW': 'euw', 'LAN': 'la1', 'LAS': 'la2', 'NA': 'na', 'OCE': 'oc', 'RU': 'ru',
            'TR': 'tr', 'JP': 'jp', 'KR': 'kr'
        }
        self._server = platforms[server]
        self._headers = {'Authorization': f'Bearer {id_token}'}

    def call(self, method, endpoint, json=None):
        url = f'https://{self._server}.store.leagueoflegends.com/storefront/v3{endpoint}'
        return request(method, url, headers=self._headers, json=json, verify=False)

    @staticmethod
    def _get_server(client):
        return client.call('GET', '/riotclient/get_region_locale').json()['region']

    @staticmethod
    def _get_id_token(client):
        return client.call('GET', '/lol-login/v1/session').json()['idToken']
