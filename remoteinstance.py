import subprocess


class RemoteInstance():
    def __init__(self, name, ip, metadata):
        self.name = name
        self.ip = ip
        self.metadata = metadata
        
        self.update_internal_status(self.check_status())

    def check_status(self):
        print("Checking status of", self.name)
        try:
            tmuxls = subprocess.check_output(['ssh', '-t', self.ip, 'tmux', 'ls'])
            tmux_vision = ('vision' in str(tmuxls))
        except Exception as e:
            tmux_vision = False
        return tmux_vision

    def update_internal_status(self, status):
        print(status)
