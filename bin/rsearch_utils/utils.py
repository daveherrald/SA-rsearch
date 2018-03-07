import os
import sys
import keyring
import ConfigParser

def _test_keys(d, conf_file):
    for k in d.keys():
        if not d[k]:
            raise ValueError("Empty value specified for option %s in config %s" % (k, conf_file))

def _parse_config(conf_file):
    """Parse config file

    Args:
        config_file: Configuration file to parse
        logger: Optional logger object
    Returns:
        Config dict
    """
    if not os.path.exists(conf_file):
        raise ValueError("Config file %s does not exist" % (conf_file)) 

    try:
        Config = ConfigParser.ConfigParser()
        parsed_conf_files = Config.read(conf_file)
    except Exception, e:
        raise ValueError("Failed to parse config file %s - %s" % (conf_file, e)) 

    USER = Config.get('rsearch', 'USER')
    SERVICE = Config.get('rsearch', 'SERVICE')
    HOST = Config.get('rsearch', 'HOST')
    PORT = Config.get('rsearch', 'PORT')
    XDG_CONFIG_HOME = Config.get('rsearch', 'XDG_CONFIG_HOME')
    XDG_DATA_HOME = Config.get('rsearch', 'XDG_DATA_HOME')
    XDG_SECRET_HOME = Config.get('rsearch', 'XDG_SECRET_HOME')

    env_vars = {"XDG_CONFIG_HOME": XDG_CONFIG_HOME,
                "XDG_DATA_HOME": XDG_DATA_HOME,
                "XDG_SECRET_HOME": XDG_SECRET_HOME}

    _test_keys(env_vars, conf_file)
    _set_env(env_vars)

    config = {"USER": USER,
              "SERVICE": SERVICE,
              "PORT": PORT,
              "HOST": HOST}

    _test_keys(config, conf_file)

    return config

def _set_env(env_vars):
    """Set environment variables used by keyring

    Args:
        env_vars: dict of environment variable names and values
    """
    for k in env_vars.keys():
        os.environ[k] = env_vars[k]

def _get_password(service, user):
    """Get password from encrypted keyring

    Args:
        service: keyring service name
        user: keyring user name

    Returns:
        password
    """
    return keyring.get_password(service, user)
