import requests
import threading
import time
from flask import Flask

from remoteinstance import RemoteInstance

app = Flask(__name__)

REMOTE = [('pi', 'pi@pi', 'Living room'), ('panda', 'pi@panda', 'Deck')]

@app.route('/')
def hello():
    return str(remote_instances[0].check_status())

def on_startup():
    global remote_instances

    remote_instances_factory = REMOTE
    
    remote_instances = [RemoteInstance(*r) for r in remote_instances_factory]

    
        

if __name__ == '__main__':
    on_startup()
    app.run()

