import os
import sys
import keyring
import ConfigParser

def _parse_config(conf_file, logger):
    #print "parsing %s" % (config)
    Config = ConfigParser.ConfigParser()
    parsed_conf_files = Config.read(conf_file)
    if not conf_file in parsed_conf_files:
       logger.error('Could not read config file: %s' % (CONF_FILE))
    USER = Config.get('rsearch', 'USER')
    SERVICE = Config.get('rsearch', 'SERVICE')
    HOST = Config.get('rsearch', 'HOST')
    PORT = Config.get('rsearch', 'PORT')
    XDG_CONFIG_HOME = Config.get('rsearch', 'XDG_CONFIG_HOME')
    XDG_DATA_HOME = Config.get('rsearch', 'XDG_DATA_HOME')
    XDG_SECRET_HOME = Config.get('rsearch', 'XDG_SECRET_HOME')

    _set_env({"XDG_CONFIG_HOME": XDG_CONFIG_HOME,
              "XDG_DATA_HOME": XDG_DATA_HOME,
              "XDG_SECRET_HOME": XDG_SECRET_HOME})

    config = {"USER": USER,
              "SERVICE": SERVICE,
              "PORT": PORT,
              "HOST": HOST}

    return config

def _set_env(env_vars):
    for v in env_vars.keys():
        os.environ[v] = env_vars[v]

def _get_password(service, user):
    return keyring.get_password(service, user)
