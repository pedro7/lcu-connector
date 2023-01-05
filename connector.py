from base64 import b64encode
from re import search
from requests import request
from subprocess import getoutput
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

class Client:
    def __init__(self):
        self._port : str
        self._headers : dict
        self.connect()

    def call(self, method, endpoint, json=None):
        url = f'https://127.0.0.1:{self._port}{endpoint}'
        return request(method, url, headers=self._headers, json=json, verify=False)

    def connect(self):
        install_directory = self._get_install_directory()
        port, password = self._get_lockfile_data(install_directory)
        auth = self._encode_password(password)
        self._port = port
        self._headers = {'Authorization' : f'Basic {auth}'}

    def _get_install_directory(self):
        try:
            client_process_args = getoutput('wmic PROCESS WHERE name="'"LeagueClientUx.exe"'" GET commandline')
            return search('--install-directory=[^"]*', client_process_args).group()[20:]
        except:
            return 'C:\Riot Games\League of Legends'

    def _get_lockfile_data(self, path):
        lockfile = open(f'{path}\lockfile').read().split(':')
        return [lockfile[2], lockfile[3]]

    def _encode_password(self, password):
        return b64encode(bytes(f'riot:{password}', 'utf-8')).decode('ascii')

class Store:
    def __init__(self):
        self._server : str
        self._headers : dict
        self.connect()

    def call(self, method, endpoint, json=None):
        url = f'https://{self._server}.store.leagueoflegends.com/storefront/v3{endpoint}'
        return request(method, url, headers=self._headers, json=json, verify=False)

    def connect(self):
        client = Client()
        server = self._get_server(client)
        id_token = self._get_id_token(client)
        servers = {'BR': 'br', 'EUNE': 'eun', 'EUW': 'euw', 'LAN': 'la1', 'LAS': 'la2', 'NA': 'na', 'OCE': 'oc', 'RU': 'ru', 'TR': 'tr', 'JP': 'jp', 'KR': 'kr'}
        self._server = servers[server]
        self._headers = {'Authorization': f'Bearer {id_token}'}

    def _get_server(self, client : Client):
        return client.call('GET', '/riotclient/get_region_locale').json()['region']

    def _get_id_token(self, client : Client):
        return client.call('GET', '/lol-login/v1/session').json()['idToken']
