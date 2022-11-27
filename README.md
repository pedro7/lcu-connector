# lcu-connector
Connects to the League of Legends Client Update so you can make requests.

## Client Usage:
~~~~ python
from connector import Client

client = Client()

client.call('request method', 'endpoint', 'data if needed')
~~~~

The code below accepts a match.

~~~~ python
from connector import Client

client = Client()

client.call('POST', '/lol-matchmaking/v1/ready-check/accept')
~~~~

To find the list of all client endpoints check: http://www.mingweisamuel.com/lcu-schema/tool/#/

## Store Usage:
~~~~ python
from connector import Store

store = Store()

store.call('request method', 'endpoint', 'data if needed')
~~~~

The code below prints your purchase history.

~~~~ python
from connector import Store

store = Store()

print(store.call('GET', '/history/purchase').json())
~~~~
