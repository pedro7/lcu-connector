from base64 import b64encode
from re import search
from requests import request
from subprocess import getoutput

class Client:
    def __init__(self):
        self.__port : str
        self.__headers : dict
        self.connect()

    def call(self, method, endpoint, json=None):
        url = f'https://127.0.0.1:{self.__port}{endpoint}'
        return request(method, url, headers=self.__headers, json=json, verify=False)

    def connect(self):
        install_directory = self.__get_install_directory()
        port, password = self.__get_lockfile_data(install_directory)
        auth = self.__encode_password(password)
        self.__port = port
        self.__headers = {'Authorization' : f'Basic {auth}'}

    def __get_install_directory(self):
        client_process_args = getoutput('wmic PROCESS WHERE name="'"LeagueClientUx.exe"'" GET commandline')
        try:
            return search('--install-directory=[^"]*', client_process_args).group()[20:]
        except AttributeError:
            return 'C:\Riot Games\League of Legends'

    def __get_lockfile_data(self, path):
        lockfile = open(f'{path}\lockfile').read().split(':')
        return [lockfile[2], lockfile[3]]

    def __encode_password(self, password):
        return b64encode(bytes(f'riot:{password}', 'utf-8')).decode('ascii')