import subprocess
import re


class RemoteInstance():
    def __init__(self, name, ip, metadata):
        print("Loading remote instance: ", name)

        self.name = name
        self.ip = ip
        self.metadata = metadata

        self.bash_prefix = ['ssh', '-t', self.ip]
        
        self.update_internal_status(self.check_status())

    def check_status(self):
        print("Checking status of", self.name)
        
        # tmuxls true/false if tmux session "vision" exists
        try:
            tmuxls = subprocess.check_output(self.bash_prefix + ['tmux', 'ls'])
            tmux_vision = ('vision' in str(tmuxls))
        except subprocess.CalledProcessError:
            tmux_vision = False
        
        # pulse_running true/false if pulseaudio is running
        try:
            pacmd_sinks = subprocess.check_output(self.bash_prefix + ['pacmd','list-sinks'])
            # pulse_running = not ('No PulseAudio' in str(pacmd_sinks))
            pulse_running = True
        except subprocess.CalledProcessError:
            pulse_running = False
            
        if tmux_vision and pulse_running:
            # awful regex to get the sink name
            remote_sink_name = re.search('name: <.*?>', str(pacmd_sinks)).group(0)[7:-1]
            pacmd_local_sinks = subprocess.check_output(['pacmd', 'list-sinks'])
            local_sink_regex = re.search('name: <tunnel.' + self.name + '.local.' +  remote_sink_name + '>', str(pacmd_local_sinks)).group(0)[7:-1]
            if local_sink_regex is None:
                print('NONE')
            else:
                print(local_sink_regex)
        else:
            pass
    
        return remote_sink_name
            
        

    def update_internal_status(self, status):
        print(status)
