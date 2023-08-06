import hid
import time

class Daemon():
    def __init__(self, vid, pid):
        self._vid = vid
        self._pid = pid
        self._hid = None
        self.raw_eps = 32
        self.commands = {}
        self.connected = False
        self.listening = False
        self.retry_duration = 15
        
    def start(self):
        self.listening = True
        while self.listening:
            self.connect()
            time.sleep(self.retry_duration)
            
    def stop(self):
        self.listening = False
        
    def connect(self):
        interfaces = hid.enumerate(self.vid, self.pid)
        filtered = [x for x in interfaces if x["interface_number"] == 1]
        if len(filtered) == 0:
            return
        path = filtered[0]["path"]
        self.hid = hid.Device(path=path)
        self.connected = True
        try:
            while self.listening:
                data = self.hid.read(self.raw_eps)
                self.call_listeners(data[0],data[1],data[2:])
        except:
            self.hid.close()
            self.hid = None
            self.connected = False
            return
        finally:
            self.hid.close()
            self.hid = None
            self.connected = False
            
    def register(self, command, subcommand, callback):
        if command > 255:
            return
        if (not subcommand is None) and subcommand > 255:
            return
        if not command in self.commands:
            self.commands[command] = {}
        if subcommand is None:
            self.commands[command]["default"] = callback
        else:
            self.commands[command][subcommand] = callback
            
    def call_listeners(self, command, subcommand, data):
        if command in self.commands:
            subcommands = self.commands[command]
            if subcommand in subcommands:
                subcommands[subcommand](command, subcommand, data)
            elif "default" in subcommands:
                subcommands["default"](command, subcommand, data)
                