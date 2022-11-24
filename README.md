# lol-client-connector
Connects to the League of Legends client API so you can make requests.

## Usage:
~~~~ python
from client import Client

client = Client()

client.call('request method', 'endpoint', 'data if needed')
~~~~

The code below accepts a match.

~~~~ python
from client import Client

client = Client()

client.call('POST', '/lol-matchmaking/v1/ready-check/accept')
~~~~

To find the list of all endpoints check: http://www.mingweisamuel.com/lcu-schema/tool/#/
