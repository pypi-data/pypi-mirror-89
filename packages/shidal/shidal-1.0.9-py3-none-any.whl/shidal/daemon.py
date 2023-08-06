import hid
import time
import os

class Daemon():
    def __init__(self, vid, pid):
        self.vid = vid
        self.pid = pid
        self.hid = None
        self.raw_eps = 32
        self.commands = {}
        self.connected = False
        self.listening = False
        self.retry_duration = 15
        
    def start(self, *args, **kwargs):
        self.listening = True
        on_connect = kwargs.get("on_connect",lambda:None)
        on_disconnect = kwargs.get("on_disconnect",lambda:None)
        while self.listening:
            self._connect(on_connect, on_disconnect)
            if self.listening:
                time.sleep(self.retry_duration)
            
    def stop(self):
        self.listening = False
        
    def _connect(self, on_connect, on_disconnect):
        interfaces = hid.enumerate(self.vid, self.pid)
        filtered = [x for x in interfaces if x["interface_number"] == 1]
        if len(filtered) == 0:
            return
        path = filtered[0]["path"]
        self.hid = hid.Device(path=path)
        self.connected = True
        on_connect()
        try:
            while self.listening:
                data = self.hid.read(self.raw_eps)
                if data and len(data) > 2:
                    self._call_listeners(data[0],data[1],data[2:])
        except Exception as e:
            pass
        finally:
            self.hid.close()
            self.hid = None
            self.connected = False
            on_disconnect()
            
    def register(self, command, subcommand, callback):
        if command > 255 or command < 0:
            return
        if (not subcommand is None) and (subcommand > 255 or subcommand < 0):
            return
        if not command in self.commands:
            self.commands[command] = {}
        if subcommand is None:
            self.commands[command]["default"] = callback
        else:
            self.commands[command][subcommand] = callback
            
    def _call_listeners(self, command, subcommand, data):
        if command in self.commands:
            subcommands = self.commands[command]
            if subcommand in subcommands:
                d = subcommands[subcommand]
            elif "default" in subcommands:
                d = subcommands["default"]
            else:
                return
            if callable(d):
                d(command, subcommand, data)
            elif isinstance(d, str):
                os.system(d)
