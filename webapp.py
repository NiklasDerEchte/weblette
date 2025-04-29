import subprocess, sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
from flask_socketio import SocketIO
from flask_cors import CORS
from flask import Flask
import configparser
import os
from datetime import timedelta

class Environment:
    def __init__(self, **kwargs):
        self._config_filename = kwargs.get("filename", "config.toml")
        self.default_settings = {
            "setup": {
                "host": "0.0.0.0",
                "port": 5000,
            },
            "flask_config": {},
            "cors": {},
            "socket": {
                "cors_allowed_origins": "*",
                "ping_timeout": 120,
                "ping_interval": 5,
            }
        }
        self.web = Flask(kwargs.get("title", "Weblette"))
        self.config = configparser.ConfigParser()
        self._setup_config(**kwargs)
        self._load_flask_config()
        self.modules = {
            "cors": CORS,
            "socket": SocketIO,
        }
    
    def add_module(self, module_name, module, settings=None):
        if module_name not in self.modules:
            if not self.config.has_section(module_name):
                self.config.add_section(module_name)
            if settings is not None:
                for option, default_value in settings.items():
                    value = default_value
                    self.config.set(module_name, option, str(value))
            self.modules[module_name] = module
        else:
            print(f"Module {module_name} already exists.")

    def _setup_config(self, **kwargs):
        if os.path.isfile(self._config_filename):
            self.config.read(self._config_filename)
        for section in self.default_settings:
            if not self.config.has_section(section):
                self.config.add_section(section)
            for option, default_value in self.default_settings[section].items():
                value = default_value
                if section in self.config and option in self.config[section]:
                    value = self.config[section][option]
                if kwargs.get(option, None) is not None:
                    value = kwargs.get(option)
                self.config.set(section, option, str(value))
        self._save_config()
    
    def _save_config(self):
        with open(self._config_filename, 'w') as f:
            self.config.write(f)
            f.close()

    def _load_flask_config(self):
        for key, value in self.config['flask_config'].items():
            try:
                time_keys = [
                    "permanent_session_lifetime", 
                    "jwt_access_token_expires", 
                    "jwt_refresh_token_expires"
                ]
                if key in time_keys:
                    value = timedelta(seconds=int(value))
                self.web.config[key.upper()] = value
            except Exception as exception:
                print(exception)

    def __getattr__(self, name):
        if name in self.modules:
            return self.modules[name]
        return None

class WebApp:
    instance = None
    def __init__(self, host=None, port=None, title=None, config_filename=None):
        params = {}
        if host is not None:
            params['host'] = host
        if port is not None:
            params['port'] = port
        if title is not None:
            params['title'] = title
        if config_filename is not None:
            params['filename'] = config_filename
        self.environment = Environment(**params)
        WebApp.instance = self
    
    def run(self):
        for module_name, module in self.environment.modules.items():
            self.environment.modules[module_name] = module(**self.environment.config._sections[module_name])
            self.environment.modules[module_name].init_app(self.environment.web)
        self.environment._save_config()
        self._demon()
    
    def _demon(self):
        try:
            host = self.environment.config['setup']['host'].strip("'").strip('"')
            port = int(self.environment.config['setup']['port'])

            print("starting weblette debug server...")
            self.environment.socket.run(self.environment.web, allow_unsafe_werkzeug=True, port=port, host=host, debug=True)
        except Exception as e:
            print("Failed to define param: {}".format(str(e)))

def make_app():
    app = WebApp()
    app.run()

if __name__ == "__main__":
    make_app()
